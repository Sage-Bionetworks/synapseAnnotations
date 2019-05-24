import os
import json
import networkx as nx
from orderedset import OrderedSet

from schema_explorer import SchemaExplorer

"""
Gather all metadata/annotations requirements for an object part of the schema.org metadata model.

Assumed semantic sugar for requirements:

- requireChildAsValue: a node property indicating that the term associated with this node
    can be set to a value equal to any of the terms associated with this node's children. 

    E.g. suppose resourceType has property requireChildAsValue set to true and suppose
    resourceType has children curatedData, experimentalData, tool, analysis. Then 
    resourceType must be set either to curatedData, experimentalData, tool, analysis.

- requiresDependency: a relationship type corresponding to an edge between two nodes/terms x and y.
    requiresDependency indicates that if a value for term x is specified, then a value for term y 
    is also required.


    E.g. suppose node experimentalData has requiresDependency edges respectively to assay and dataType.
    Then, if experimentalData is specified that requires that both assay and dataType are specified
    (e.g. in annotations of an object).


This semantic sugar enables the generation different kinds of validation schemas including:
    - validate that all required annotation terms (i.e. properties) of an object are present in the 
    annotations json file associated with this object
    - validate that the value provided for a given property of an object is within a set of admissible values
    for that property
    - validate conditional annotations: if a property of an object is set to a specific value x, check if value 
    x requires any additional annotation properties to be specified for this object. E.g. if resourceType
    is experimentalData, require also that annotations/properties assay, dataType are set. 
    This support cascades of conditional validation (of arbitrary lengths).
"""


"""
Starting from a root node, get all nodes reachable on requiresDependency edges
"""
def get_requirements_subgraph(mm_graph, root):

    # get all nodes reachable from the specified root node in the data model
    # TODO: catch if root is not in graph?
    root_descendants = nx.descendants(mm_graph, root)

    # get the subgraph induced on all nodes reachable from the root node
    descendants_subgraph = mm_graph.subgraph(list(root_descendants))

    '''
    prune the descendants subgraph to include only requireDependency edges
    '''
    req_edges = []
    for u, v, properties in descendants_subgraph.edges(data = True):
        if properties["relationship"] == requires_dependency:
            req_edges.append((u,v))
    
    requirements_subgraph = descendants_subgraph.edge_subgraph(req_edges)

    # get only the nodes reachable from the root node (after the pruning above
    # some nodes in the root-descendants subgraph might have become disconnected)
    requirements_subgraph = nx.descendants(requirements_subgraph, root)
    
    return requirements_subgraph


"""
Get the parent-children out-edges of a node: i.e. edges connecting to nodes neighbors
of node u on edges of type "parentOf"
"""
def get_children_edges(mm_graph, u):

    children_edges = []
    for u, v, properties in mm_graph.out_edges(u, data = True):
        if properties["relationship"] == "parentOf": 
            children_edges.append((u,v))

    return children_edges



"""
Get the children nodes of a node: i.e. nodes neighbors of node u
on edges of type "parentOf"
"""
def get_node_children(mm_graph, u):

    children = set()
    for u, v, properties in mm_graph.out_edges(u, data = true):
        if properties["relationship"] == "parentof": 
            children.add(v)

    return list(children)


"""
Get the nodes that this node requires as dependencies that are also neihbors of node u
on edges of type "requiresDependency"
"""
def get_node_neighbor_dependencies(mm_graph, u):
    
    children = set()
    for u, v, properties in mm_graph.out_edges(u, data = true):
        if properties["relationship"] == requires_dependency: 
            children.add(v)

    return list(children)


"""
Get the nodes that this node requires as dependencies.
These are all nodes *reachable* on edges of type "requiresDependency"
"""
def get_node_dependencies(req_graph, u):
    
    descendants = nx.descendants(req_graph, u)

    return list(descendants)


"""
Gather dependencies and value-constraints across terms/nodes in 
a schema.org schema and store them as a JSONSchema schema. 
I.e. recursively, for any given node in the schema.org schema starting at a root
node, 1) find all the terms that this node depends on (and hence are required as 
additional metadata, given this node is required); 2) find all the 
allowable metadata values/nodes that can be assigned to a particular node
(if such constraint is specified in the schema)
"""
def get_JSONSchema_requirements(se, root):
    
    json_schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "$id":"http://example.com/" + root + "JSONSchema",
          "title": root + "JSONSchema",
          "type": "object",
          "properties":{},
          "required":[]
    }

    # get graph corresponding to data model schema
    mm_graph = se.get_nx_schema()

    # get requirements subgraph
    req_graph = get_requirements_subgraph(mm_graph, root)

    nodes_to_process = OrderedSet()
    nodes_to_process.add(root) 

    '''
    keep checking for dependencies until there are no nodes
    left to process
    '''
    while nodes_to_process:  
        process_node = nodes_to_process.pop()

        '''
        get allowable values for this node;
        each of these values is a node that in turn is processed for
        dependencies and allowed values
        '''
        if requires_child in mm_graph[process_node]:
            if mm_graph[process_node][requires_child] == "True":
                children = get_node_children(mm_graph, process_node)
                
                # set allowable values based on children nodes
                schema_properties = { process_node:{"enum":children}}
                json_schema["properties"].update(schema_properties)                
                
                # add children for requirements processing
                nodes_to_process.update(children)
                
                # set conditional dependencies based on children dependencies
                for child in children:
                    child_dependencies = get_node_dependencies(req_graph, child)
                    schema_conditional_dependencies = {
                            "if": {
                                "properties": {
                                process_node: { "enum": [child] }
                                }       
                              },
                            "then": { "required": [child_dependencies] },
                    }

                    json_schema.update(schema_conditional_dependencies)

        '''
        get required nodes by this node (e.g. other terms/nodes
        that need to be specified based on a data model, if the 
        given term is specified); each of these node/terms needs to be 
        processed for dependencies in turn.
        '''
        process_node_dependencies = get_node_dependencies(req_graph, process_node)

        if process_node_dependencies:
            if process_node == root: # these are unconditional dependencies 
                json_schema["required"] += process_node_dependencies
            else: # these are dependencies given the processed node 
                schema_conditional_dependencies = {
                        "if": {
                            "properties": {
                            process_node: { "enum": #TODO "" }
                            }       
                          },
                        "then": { "required": [process_node_dependencies] },
                }

                json_schema.update(schema_conditional_dependencies)

            nodes_to_process.update(process_node_dependencies)

    return json_schema




"""
###############################################
===============================================
###############################################
"""

json_schema_output_dir = "./schemas"
schemaorg_schema_input_dir = "./data"
requires_dependency = "requiresDependency"
requires_child = "requiresChildAsValue"

    
if __name__ == "__main__":

    schemaorg_schema_file_name = "./data/masterSageGeneralRequirements.jsonld"

    se = SchemaExplorer()
    se.load_schema(os.path.join(schemaorg_schema_input_dir, schemaorg_schema_file_name))

    jsonSchema = get_JSONSchema_requirements(se, "requirementsNF")

    

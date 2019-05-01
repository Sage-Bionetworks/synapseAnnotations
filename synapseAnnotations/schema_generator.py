"""
utility functions to genereate jsonSchema validation schemas based on 
a data model in a schema.org/biothings format

see jsonld_2_jsonschema.py file for example usage
"""

import os
import json
import networkx as nx

from schema_explorer import SchemaExplorer


# validation schemas output folder
schemas_path = "./schemas"

"""
gather all metadata requirements part of the schema.org metadata model
assume the requirements are specified in a dictionary format

requirements = {<requirementType>:[<requirementTerms>]}

for now, ad hoc, the requirements dict is passed as a parameter
"""
def generate_requirements(se, requirements):

    req_model = {}
    for req_type, req_terms in requirements.items():

        # this logic can be abstracted in a factory pattern
        # when we have better defined requirements semantics
        if req_type == "type" and "requiresChild" in req_terms:
            req_model = generate_requires_child_model(se, req_model)
        
        if req_type == "type" and "requiresProperty" in req_terms:
            req_model = generate_requires_property_model(se, req_model)
        
        generate_json_schema("enum", req_model)    


def generate_requires_child_model(se, req_model):

    mm_graph = se.get_nx_schema()

    for node, properties in mm_graph.nodes(data = True):
        if "requiresChild" in properties:
             
            print("Added node " + node + " to requirements.")
            children = mm_graph.neighbors(node)
            req_model[node] = {}
            req_model[node]["properties"] = list(children)
            if "jsonType" in properties:
                req_model[node]["type"] = properties["jsonType"]

    return req_model


def generate_requires_property_model(se, req_model):

    mm_graph = se.get_nx_schema()

    for node, properties in mm_graph.nodes(data = True):
        if "requires" in properties:
            req_properties = properties["requires"]
            req_model[node] = {}
            req_model[node]["properties"] = req_properties
            if "jsonType" in properties:
                req_model[node]["type"] = properties["jsonType"]
    
    return req_model


def generate_enum_schema(req_model):

        schema_properties = {"properties": {}}
        
        for term, req in req_model.items():
            req_properties = req["properties"]

            json_type = "string"
            if "type" in req:
                json_type = req["type"]
           

            schema_properties["properties"].update({
                    term:{"type":json_type, 
                          "enum":list(req_properties)
                    }
            })

        return schema_properties



def generate_json_schema(schema_type, req_model):

  
    # name of output validation schema...

    schema_name = "masterSageJSONSchema.json"
    
    # hardcoded boilerplate; all of this can be refactored
    json_schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "$id":"http://example.com/"+schema_name,
          "title": "jsonSchema",
          "type": "object"
    }


    if schema_type == "enum":
        
        schema_properties = generate_enum_schema(req_model)
        json_schema.update(schema_properties)

    
    print("=========================================")
    print("Generated all requirements")
    print("=========================================")

    schema_path = os.path.join(schemas_path, schema_name)

    with open(schema_path, "w") as sf:
        json.dump(json_schema, sf, indent = 3)


    print("JSON schema generated and stored at")
    print(schema_path)


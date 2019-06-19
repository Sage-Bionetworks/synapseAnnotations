import os
import json

from PIL import Image
from schema_explorer import SchemaExplorer
import pprint as pp
from graphviz import Source
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph

def get_descendents_subgraph(G, node_id):

    s = [node_id]
    for v in dict(nx.bfs_successors(G, node_id)).values():
        s += v
    s = set(s)

    return G.subgraph(s)


def topic_node_style(G, node_id):

    G.node[node_id]["shape"] = "tripleoctagon"
    G.node[node_id]["fontsize"] = "52"
    G.node[node_id]["fontname"] = "Arial bold"


def get_class(class_name, description = None, subclass_of = "Thing"):
    
    class_attributes = {
                    '@id': 'bts:'+class_name,
                    '@type': 'rdfs:Class',
                    'rdfs:comment': description if description else "",
                    'rdfs:label': class_name,
                    'rdfs:subClassOf': {'@id': 'bts:' + subclass_of},
                    'schema:isPartOf': {'@id': 'http://schema.biothings.io'}
    }

    return class_attributes

def first_upper(s):
    return s[0].upper() + s[1:] if len(s) > 0 else s


# path to Synapse annotations
annotations_path = "./data"
annotations_file = "cancer.json"
output_schema_name = "NFSchema"
base_schema_org_file = "NFSchema.jsonld"


# instantiate schema explorer
se = SchemaExplorer()
se.load_schema(os.path.join(annotations_path, base_schema_org_file))


# add adhoc classes; TODO: this should be generated based on a metadata model schema

# experimentalData classes
'''
new_class = get_class("assay",\
          description = "The technology used to generate the data in this file",\
          subclass_of = "Thing"\
)
se.update_class(new_class)
'''
'''
new_class = get_class("dataEntity",\
          description = "A data derived entity and attributes.",\
          subclass_of = "EvidenceType"\
)
se.update_class(new_class)


new_class = get_class("data",\
          description = "A piece of data (e.g. from an assay).",\
          subclass_of = "dataEntity"\
)
se.update_class(new_class)

new_class = get_class("behavioralEntity",\
          description = "Entity and attributes derived from a Behavior",\
          subclass_of = "Thing"\
)
se.update_class(new_class)


new_class = get_class("metabolicEntity",\
          description = "Entity and attributes derived from molecular metabolics",\
          subclass_of = "molecularEntity"\
)
se.update_class(new_class)

new_class = get_class("proteomicEntity",\
          description = "Entity and attributes derived from molecular proteomics",\
          subclass_of = "molecularEntity"\
)
se.update_class(new_class)

new_class = get_class("proteomicEntity",\
          description = "Entity and attributes derived from molecular proteomics",\
          subclass_of = "molecularEntity"\
)
se.update_class(new_class)

class_info = se.explore_class("Device")
edit_class = get_class("Device",\
          description =  class_info["description"],\
          subclass_of = "assay"\
)
se.edit_class(edit_class)
'''

'''
# ngs classes
new_class = get_class("nextGenerationSequencing",\
          description = "Technologies that facilitate the rapid determination of the DNA sequence of large numbers of strands or segments of DNA. [def-source: NCI]",\
          subclass_of = "assay"\
)
se.update_class(new_class)
'''
'''
#tools classes
new_class = get_class("tool",\
          description = "Software code or artifact tool",\
          subclass_of = "Thing"\
)
se.update_class(new_class)
'''

# cancer classes
new_class = get_class("cancer",\
          description = "A tumor composed of atypical neoplastic, often pleomorphic cells that invade other tissues. Malignant neoplasms often metastasize to distant anatomic sites and may recur after excision. The most common malignant neoplasms are carcinomas (adenocarcinomas or squamous cell carcinomas), Hodgkin and non-Hodgkin lymphomas, leukemias, melanomas, and sarcomas.",\
          subclass_of = "diagnosis"\
)
se.update_class(new_class)


# load existing Synapse annotations and convert them to BioThings
# augmenting existing BioThings schema

with open(os.path.join(annotations_path, annotations_file), "r") as a_f:
    synapse_annotations = json.load(a_f)

for annotations_entity in synapse_annotations:

    if not "biothingsParent" in annotations_entity:
        continue

    #class_name = first_upper(annotations_entity["name"])
    class_name = annotations_entity["name"]
    subclass_of = annotations_entity["biothingsParent"]
    description = annotations_entity["description"]

    new_class = get_class(class_name,\
                          description = description,\
                          subclass_of = subclass_of\
    )
    se.update_class(new_class)
    
    if len(annotations_entity["enumValues"]) > 0 and annotations_entity["columnType"] != "BOOLEAN":  

        for nested_entity in annotations_entity["enumValues"]:
            subclass_of = class_name
            if nested_entity["value"] == "Not Applicable": 
                continue

            #nested_class_name = first_upper(nested_entity["value"])
            nested_class_name = nested_entity["value"]
            nested_description = nested_entity["description"]
            new_class = get_class(nested_class_name,\
                                  description = nested_description,\
                                  subclass_of = subclass_of\
            )
            se.update_class(new_class)

            if "biothingsParent" in nested_entity:
                subclass_of = nested_entity["biothingsParent"]
                new_class = get_class(nested_class_name,\
                                  description = nested_description,\
                                  subclass_of = subclass_of\
                )
                se.update_class(new_class)


'''
nx.set_node_attributes(se.schema_nx, "red",  "fillcolor")

color1_subgraph = get_descendents_subgraph(se.schema_nx, "Assay")

nx.set_node_attributes(color1_subgraph, "#990000",  "fillcolor")
nx.set_node_attributes(color1_subgraph, "#990000",  "color")
nx.set_edge_attributes(color1_subgraph,"#990000", "color")  
nx.set_node_attributes(color1_subgraph, "32",  "fontsize")

topic_node_style(color1_subgraph, "Assay")


color2_subgraph = get_descendents_subgraph(se.schema_nx, "Platform")

nx.set_node_attributes(color2_subgraph, "#ff9900",  "fillcolor")
nx.set_node_attributes(color2_subgraph, "#ff9900",  "color")
nx.set_edge_attributes(color2_subgraph,"#ff9900", "color")  
topic_node_style(color2_subgraph, "Platform")


color3_subgraph = get_descendents_subgraph(se.schema_nx, "AssayTarget")

topic_node_style(color3_subgraph, "AssayTarget")
#topic_node_style(color3_subgraph, "CellType")

nx.set_node_attributes(color3_subgraph, "#006600",  "fillcolor")
nx.set_node_attributes(color3_subgraph, "#006600",  "color")
nx.set_edge_attributes(color3_subgraph,"#006600", "color")  

display_subgraph = get_descendents_subgraph(se.schema_nx, "Assay")

#topic_node_style(display_subgraph, "AnatomicalEntity")

agraph = to_agraph(display_subgraph)
agraph.graph_attr['overlap']='false'
agraph.node_attr['style'] = "filled"
agraph.layout(prog = "fdp")
agraph.draw("color.pdf")
#img = Image.open('color.png')
#img.show()
'''
'''
full_schema = se.full_schema_graph()
full_schema.engine = "fdp"
full_schema.render(filename=os.path.join(annotations_path, output_schema_name), view = True)
'''
partial_schema = se.sub_schema_graph(source="assay", direction="down")
partial_schema.engine = "circo"
partial_schema.render(filename=os.path.join(annotations_path, "partial_" +output_schema_name), view = True)

se.export_schema(os.path.join(annotations_path, output_schema_name + ".jsonld"))


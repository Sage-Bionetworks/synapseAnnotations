"""
generate jsonSchema validation schemas from existing datamodel
see schema_generator for helper methods used here
"""

import os
import json

from schema_explorer import SchemaExplorer
import pprint as pp
import networkx as nx
from schema_generator import generate_requirements

if __name__ == "__main__":

    # path to Synapse annotations
    annotations_path = "./data"
    base_schema_org_file = "masterSageMoreRequirements.jsonld"
    #base_schema_org_file = "masterSage.jsonld"
    #base_schema_org_file = "masterSageTargetRequirements.jsonld"


    # instantiate schema explorer
    se = SchemaExplorer()
    se.load_schema(os.path.join(annotations_path, base_schema_org_file))


    '''
    # visualize default schema
    full_schema = se.full_schema_graph()
    full_schema.render(filename=os.path.join(annotations_path, annotations_file + "biothings_schema"), view = True)
    '''

    #generate_requirements(se, {"type":["requiresChild", "requiresProperty"]})
    generate_requirements(se, {"type":["requiresChild"]})


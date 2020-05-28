"""
Ad-hoc code converting vocabularies in the Sage annotation style to csv template suitable for defining schema.org schemas
"""

import os
import json

import pandas as pd

# path to Synapse annotations
annotations_path = "./data"

# Sage annotations file(s) to convert to schema.org
annotation_files = [
            "experimentalData.json",
            "cancer.json",
            "neuro.json",
            "neurofibromatosis.json",
            "ngs.json",
            "chem.json",
            "compoundScreen.json",
            "curatedData.json",
            "dhart.json",
            "genie.json",
            "array.json",
            "analysis.json",
            "sageCommunity.json",
            "network.json",
            "tool.json",
            "toolExtended.json",
            "immunoAssays.json"
] 


# load existing Synapse annotations and convert them to a csv format that can be translated into 
# a Schema.org json-ld schema augmenting the existing BioThings schema

# the csv contains the following minimal headers
# note: the existing controlled vocabulary doesn't provide sufficient 
# information to fill all of these columns; 
# the conversion script csv_2_schemaorg.py can handle that, however the data model encoded in the
# end schema will be incomplete

headers = ["Attribute", "Description", "Valid Values", "Requires", "Properties", "Required", "Parent", "Requires Component", "Source"]
entity_idx = 0
csv_schema = {}

# go over annotation files and extract all annotation attributes to store in the schema
for annotation_file in annotation_files:

    print("===============")
    print("Processing file " + annotation_file)

    # since we don't have the biothings parent of annotation attributes, we assume 
    # the file (e.g. experimentalData) is itself an attribute with parent Thing in the 
    # BioThings hierarchy; this attribute may represent a component grouping topically 
    # attributes in our data model. We can adjust as we develop the data model
    component_attribute_name = annotation_file.split(".")[0]
    print("Adding component " + component_attribute_name) 
    
    # by default assume an attribute/annotation key is not required
    csv_schema[entity_idx] = [component_attribute_name, "", "", "", "", "FALSE", "", "", ""]

    #increment entity index
    entity_idx += 1
    print("===============")

    with open(os.path.join(annotations_path, annotation_file), "r") as a_f:
        synapse_annotations = json.load(a_f)

    for annotations_entity in synapse_annotations:

        attribute_name = annotations_entity["name"]

        print("- Getting info for attribute " + attribute_name)

        # since we don't know what the BioThings parent of our entity is we set the parent to be 
        # the component attribute (i.e. annotations base filename extracted above); we can adjust accordingly the parent of the core elements directly in the csv
        subclass_of = component_attribute_name
        description = annotations_entity["description"]
        source = ""
        if "source" in annotations_entity and annotations_entity["source"]:
            source = annotations_entity["source"]

        # getting valid values (i.e. range of this attribute)
        valid_values = ""
        if "enumValues" in annotations_entity and len(annotations_entity["enumValues"]) > 0:  

            for nested_entity in annotations_entity["enumValues"]:
                
                nested_attribute_name = nested_entity["value"]

                # assuming this attribute name is a valid value for parent attribute
                valid_values +=  str(nested_attribute_name) if not valid_values else ", " + str(nested_attribute_name)

                # add attribute to schema (if not itself a primitive type like boolean)
                if ("columnType" in annotations_entity and annotations_entity["columnType"] == "BOOLEAN") or nested_entity["value"] == "Not Applicable":
                    continue
                
                print("--- Getting info for attribute " + str(nested_attribute_name))
                nested_subclass_of = attribute_name
                nested_description = nested_entity["description"]
                nested_source = ""
                if "source" in nested_entity and nested_entity["source"]:
                    nested_source = nested_entity["source"]

                
                # adding attribute to schema
                csv_schema[entity_idx] = [nested_attribute_name, nested_description, "", "", "", "FALSE", nested_subclass_of, "", nested_source]
                
                print("--- Added attribute " + str(nested_attribute_name) + " for parent " + nested_subclass_of)

                # increment entity index
                entity_idx += 1

        # add parent/outer attribute to schema
        csv_schema[entity_idx] = [attribute_name, description, valid_values, "", "", "TRUE", subclass_of, "", source]

        print("- Added parent " + attribute_name + " for parent " + subclass_of)
        entity_idx += 1

# construct a data frame containing this preliminary schema
schema = pd.DataFrame.from_dict(csv_schema, orient = "index", columns = headers)
schema.to_csv("sage_controlled_vocabulary_schema.csv", index = False)

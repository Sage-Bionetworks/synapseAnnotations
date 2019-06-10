import os
import json
import pprint
  
from schema_explorer import SchemaExplorer

def get_class(class_name, description = None, subclass_of = "Thing", requires_dependencies = None, requires_value = None):

    class_attributes = {
                    '@id': 'bts:'+class_name,
                    '@type': 'rdfs:Class',
                    'rdfs:comment': description if description else "",
                    'rdfs:label': class_name,
                    'rdfs:subClassOf': {'@id': 'bts:' + subclass_of},
                    'schema:isPartOf': {'@id': 'http://schema.biothings.io'}
    }

    if requires_dependencies:
        requirement = {'rdfs:requiresDependency':[{'@id':'sms:' + dep} for dep in requires_dependencies]}
        class_attributes.update(requirement)

    if requires_value != None:
        value_constraint = {'rdfs:requiresChildAsValue':{'@id':'sms:' +  str(requires_value)}}
        class_attributes.update(value_constraint)
    
    return class_attributes


def get_property(property_name, property_class_name, description = None, allowed_values = 'Text'):

    new_property = {
                    '@id': 'bts:' + property_name,
                    '@type': 'rdf:Property',
                    'rdfs:comment': description if description else "",
                    'rdfs:label': property_name,
                    'schema:domainIncludes': {'@id': 'bts:' + property_class_name},
                    'schema:rangeIncludes': {'@id': 'schema:' + allowed_values},
                    'schema:isPartOf': {'@id': 'http://schema.biothings.io'},
    }
                    
    #'http://schema.org/domainIncludes':{'@id': 'bts:' + property_class_name},
    #'http://schema.org/rangeIncludes':{'@id': 'schema:' + allowed_values},
    

    return new_property


# path to Synapse annotations
annotations_path = "./data"
output_schema_name = "NFSchemaReq"
base_schema_org_file = "NFSchema.jsonld"


# instantiate schema explorer
se = SchemaExplorer()
se.load_schema(os.path.join(annotations_path, base_schema_org_file))

"""
# edit class to add a requirement
"""

class_info = se.explore_class("resourceType")

class_req_edit = get_class("resourceType",\
                              description = class_info["description"],\
                              subclass_of = "Thing",\
                              requires_value = True  

)
se.edit_class(class_req_edit)


class_info = se.explore_class("Thing")
class_req_edit = get_class("Thing",\
                              description = class_info["description"],\
                              subclass_of = "Thing",\
                              requires_dependencies = ["resourceType", "consortium", "fileFormat", "fundingAgency"]

)
se.edit_class(class_req_edit)

# TODO: fix schema that requires subClassOf property for class Thing (Thing cannot be a class of itself

class_info = se.explore_class("experimentalData")
class_req_edit = get_class("experimentalData",\
                              description = class_info["description"],\
                              subclass_of = class_info["subClassOf"],\
                              requires_dependencies = ["assay", "dataType", "dataSubtype", "specimenID", "individualID", "species", "isCellLine", "sex", "diagnosis"]\
)
se.edit_class(class_req_edit)


class_info = se.explore_class("diagnosis")
class_req_edit = get_class("diagnosis",\
                              description = class_info["description"],\
                              subclass_of = class_info["subClassOf"],\
                              requires_value = True\
) 
se.edit_class(class_req_edit)


diseases = se.find_child_classes("diagnosis")

print("=============")
print("Setting requirements for diseases")
print("=============")
for disease in diseases:
    if not "cancer" in disease.lower() and not "leukemia" in disease.lower():
        print(disease)
        class_info = se.explore_class(disease)
        class_req_edit = get_class(disease,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["tissue"]\
        )
        se.edit_class(class_req_edit)
    else:
        print(disease)
        class_info = se.explore_class(disease)
        class_req_edit = get_class(disease,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["tumorType"]\
        )
        se.edit_class(class_req_edit)

        

class_info = se.explore_class("cancer")
class_req_edit = get_class("cancer",\
                              description = class_info["description"],\
                              subclass_of = "diagnosis",\
                              requires_dependencies = ["tumorType"]\
)
se.edit_class(class_req_edit)

class_info = se.explore_class("assay")
class_req_edit = get_class("assay",\
                              description = class_info["description"],\
                              subclass_of = class_info["subClassOf"],\
                              requires_value = True\
) 
se.edit_class(class_req_edit)

print("=============")
print("Setting requirements for assays")
print("=============")


assays = se.find_child_classes("assay")
for assay in assays:
    if "seq" in assay.lower():
        print(assay)
        class_info = se.explore_class(assay)
        class_req_edit = get_class(assay,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["platform", "readLength", "readPairOrientation", "runType", "isStranded", "dissociationMethod", "nucleicAcidSource", "libraryPrep", "libraryPreparationMethod"]\
        )
        se.edit_class(class_req_edit)

    if "array" in assay.lower():
        print(assay)
        class_info = se.explore_class(assay)
        class_req_edit = get_class(assay,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["platform"]\
        )
        se.edit_class(class_req_edit)

    if assay.lower() in ["westernblot", "immunohistochemistry", "chipseq"]:
        print(assay)
        class_info = se.explore_class(assay)
        class_req_edit = get_class(assay,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["assayTarget"]\
        )
        se.edit_class(class_req_edit)

        class_info = se.explore_class(assay)
        class_req_edit = get_class(assay,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["assayTarget"]\
        )
        se.edit_class(class_req_edit)

    if assay == "cellViabilityAssay":
        class_info = se.explore_class(assay)
        class_req_edit = get_class(assay,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_dependencies = ["chemicalStructure"]\
        )
        se.edit_class(class_req_edit)
        

print("=============")
print("Setting requirements for NGS properties")
print("=============")

ngs_props = se.find_child_classes("nextGenerationSequencing") 
print(ngs_props)
for ngs_prop in ngs_props:
        print(ngs_prop)
        class_info = se.explore_class(ngs_prop)
        class_req_edit = get_class(ngs_prop,\
                                      description = class_info["description"],\
                                      subclass_of = class_info["subClassOf"],\
                                      requires_value = True
        )
        se.edit_class(class_req_edit)



class_info = se.explore_class("assayTarget")
class_req_edit = get_class("assayTarget",\
                              description = class_info["description"],\
                              subclass_of = class_info["subClassOf"],\
                              requires_value = True\
)
se.edit_class(class_req_edit)


class_info = se.explore_class("tool")
class_req_edit = get_class("tool",\
                              description = class_info["description"],\
                              subclass_of = "resourceType",\
                              requires_dependencies = ["softwareName", "softwareType", "softwareLanguage", "softwareRepository", "inputDataType", "outputDataType"]\
)
se.edit_class(class_req_edit)


"""
diagnosis, if diseased; what the key for diseased?
"""

'''
# One can examine any class/node in the schema.
# example of class exploration
pp = pprint.PrettyPrinter(indent=4)
class_info = se.explore_class('Individual')
pp.pprint(class_info)
'''
'''
# draw schema parentOf relationship graph

partial_schema = se.sub_schema_graph(source="resourceType", direction="down")
partial_schema.engine = "circo"
partial_schema.render(filename=os.path.join(annotations_path, "partial_" +output_schema_name), view = True)
'''


# saving updated schema 
se.export_schema(os.path.join(annotations_path, output_schema_name + ".jsonld"))


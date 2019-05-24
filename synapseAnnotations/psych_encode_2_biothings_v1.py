import os
import json
import pprint
  
from schema_explorer import SchemaExplorer

def get_class(class_name, description = None, subclass_of = "Thing", requires_dependency = None, requires_value = None):
    
    class_attributes = {
                    '@id': 'bts:'+class_name,
                    '@type': 'rdfs:Class',
                    'rdfs:comment': description if description else "",
                    'rdfs:label': class_name,
                    'rdfs:subClassOf': {'@id': 'bts:' + subclass_of},
                    'schema:isPartOf': {'@id': 'http://schema.biothings.io'}
    }

    if requires_dependency:
        requirement = {'rdfs:requiresDependency':{'@id':'sms:' +  requires_dependency}}
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



# make this directory if you haven't already
# it stores the output schema
annotations_path = "./data"

# schema name: can be changed as needed
schema_name = "psychENCODE"


# instantiate schema explorer
se = SchemaExplorer()

# visualize biothings schema
print("Visualizing BioThings schema...")
full_schema = se.full_schema_graph()
full_schema.render(filename=os.path.join(annotations_path, "biothings_schema.pdf"), view = True)
print("Done")


print("Adding psychENCODE nodes...")

'''
# add classes/nodes matching psychENCODE manifest specifications in
#
# https://docs.google.com/spreadsheets/d/1ZCDysCGgE_RvePPiAAp1cylUE5C0MmSX_GHDJjILkzQ/edit?usp=sharing
#
# to the Biothings base ontology
#
# for now we are hard-coding definitions; however, in the future we should have URI for each term and definition used in a dictionary
# e.g. see https://schema.org/docs/schema_org_rdfa.html
 
# please check if a class already exist in the BioThings schema (either in data/biothings_schema.pdf or in this dictionary 
# http://discovery.biothings.io/bts29009/

# if the class does not exist, extend the BioThings schema with related nodes, which can then be 
# used to add PsychEncode nodes

example: DataEntity does not exist as a term in Biothings, but is useful as an umbrella
term/node/object/class for Data artifacts like Dataset, File, FASTQ, etc.
so we add DataEntity as a subclass under the EvidenceType term in Biothings
'''

new_class = get_class("DataEntity",\
          description = "A data derived entity and attributes.",\
          subclass_of = "EvidenceType",\
          requires_dependency = "EvidenceType",\
          requires_value = True
)
se.update_class(new_class)

'''
Data is even more specific term, as noted above;
so we add it to the ontology
'''
new_class = get_class("Data",\
          description = "A piece of data (e.g. from an assay).",\
          subclass_of = "DataEntity",\
)
se.update_class(new_class)


'''
similarly, we could add various entities to the biothings ontology 
in expectation of the attributes relevant for PsychENCODE; some of the terms above may be 
relevant others less so; it is up to the curator to decide what to include and what not
based on the psychENCODE manifest
'''
'''
new_class = get_class("BehavioralEntity",\
          description = "Entity and attributes derived from a Behavior",\
          subclass_of = "Thing"\
)
se.update_class(new_class)


new_class = get_class("MetabolicEntity",\
          description = "Entity and attributes derived from molecular metabolics",\
          subclass_of = "MolecularEntity"\
)
se.update_class(new_class)

new_class = get_class("ProteomicEntity",\
          description = "Entity and attributes derived from molecular proteomics",\
          subclass_of = "MolecularEntity"\
)
se.update_class(new_class)


new_class = get_class("Organization",\
          description =  "An organization such as a school, NGO, corporation, club, etc." ,\
          subclass_of = "Thing"\
)
se.update_class(new_class)



# Organization-related nodes
new_class = get_class("Study",\
          description =  "Grant research unit" ,\
          subclass_of = "Organization"\
)
se.update_class(new_class)

new_class = get_class("Consortium",\
          description =  "Consortium name" ,\
          subclass_of = "Organization"\
)
se.update_class(new_class)

new_class = get_class("Grant",\
          description =  "NIH project number" ,\
          subclass_of = "Study"\
)
se.update_class(new_class)


new_class = get_class("Investigator",\
          description =  "Principal investigator on a project" ,\
          subclass_of = "Person"\
)
se.update_class(new_class)
'''

"""
'''
Individual is one of the more important terms in the PsychENCODE 
manifest and we extend the Biothings schema correspondingly;
Individual is a subclass of a Case; but the curator may change that and 
have the individual as a subclass of a Organism; Individual can have multiple parent 
terms as well. Simply add the Individual term as a new class once for each 
of its parents.
'''
new_class = get_class("Individual",\
          description =  "Donor individual" ,\
          subclass_of = "Case"\
)
se.update_class(new_class)
"""

"""
'''
Suppose we'd like to add properties to an existing class/term, e.g. Individual
The template below allows the addition of a property one at a time. For instance,
IndividualAccession, IndividualID, etc.
'''
# add individual properties
new_property = get_property("IndividualAccession",\
                            "Individual",\
                            description = "Unique donor ID assigned by DAC.DCC"\
)
se.update_property(new_property)

new_property = get_property("IndividualID",\
                            "Individual",\
                            description = "Donor ID as provided by lab"\
)
se.update_property(new_property)

new_property = get_property("IndividualIDSource",\
                            "Individual",\
                            description = "Brain bank or other repository to which individualID maps"\
)
se.update_property(new_property)

new_property = get_property("Species",\
                            "Individual",\
                            description = "The name of this Individual species"\
)
se.update_property(new_property)

new_property = get_property("ReportedGender",\
                            "Individual",\
                            description = "Gender as reported by brain bank"\
)
se.update_property(new_property)

new_property = get_property("Sex",\
                            "Individual",\
                            description = "SNP Genotype"\
)
se.update_property(new_property)

new_property = get_property("Age",\
                            "Individual",\
                            description = "Age of individual at biospecimen sampling - age of death for postmortem tissue"\
)
se.update_property(new_property)

new_property = get_property("AgeUnits",\
                            "Individual",\
                            description = "The unit of measurement (gestational week or year)"\
)
se.update_property(new_property)

new_property = get_property("Race",\
                            "Individual",\
                            description = "A person’s social group identification"\
)
se.update_property(new_property)


new_property = get_property("RaceDetail",\
                            "Individual",\
                            description = "Hispanic or Latino and Not Hispanic or Latino"\
)
se.update_property(new_property)

new_property = get_property("GenotypeInferredAncestry",\
                            "Individual",\
                            description = "Ancestry inferred from genotype"\
)
se.update_property(new_property)


new_property = get_property("IQ",\
                            "Individual",\
                            description = "Individuals IQ"\
)
se.update_property(new_property)


new_property = get_property("BMI",\
                            "Individual",\
                            description = "Body Mass Index"\
)
se.update_property(new_property)
"""

"""
'''
One can examine any class/node in the schema.
# example of class exploration
'''
pp = pprint.PrettyPrinter(indent=4)
class_info = se.explore_class('Individual')
pp.pprint(class_info)
"""

"""
'''
Once done editing the schema we can visualize it 
'''
print("Visualizing psychENCODE schema...")
full_schema = se.full_schema_graph()
full_schema.engine = "fdp"
full_schema.render(filename=os.path.join(annotations_path, schema_name + "_schema.pdf"), view = True)
print("Done")
"""

"""
# example of visualizing part of a schema
partial_schema = se.sub_schema_graph(source="Assay", direction="down")
partial_schema.engine = "circo"
partial_schema.render(filename=os.path.join(annotations_path, schema_name + "_partial_schema.pdf"), view = True)
"""

# saving updated schema 
se.export_schema(os.path.join(annotations_path, schema_name + ".jsonld"))

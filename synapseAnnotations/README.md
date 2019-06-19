# README

This subfolder contains our annotation controlled vocabularies, schemas, and
code to generate schemas based on existing JSON files, as well as code to generate
JSONSchema schemas from schema.org schemas.


## Installation 

- Clone this branch of the repo.
- Install dependencies (e.g. pip or conda; either should work):
  * networkx
  * rdflib
  * tabletext
  * graphviz (this is for visualization only)
  * jsonschema
  * orderedset
  * google-api-python-client
  * google-auth-httplib2 
  * google-auth-oauthlib

- We use ajv for testing example JSONSchemas; you can install via nodejs and npm


## Converting existing annotations to JSON-LD Schema.org schemas

To translate our original JSON files to JSON-LD requires the following steps:

1. Run `utilities/sage_annotations_2_biothings.py`. Running this on a single [input JSON file](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L55)
will take that file, add it to the Biothings schema, and save the result to a
file with the same base file name as the original (e.g. `data/original/sageCommunity.json`
becomes `data/jsonld-data-model/sageCommunity.jsonld`). The script can also append additional data to a
JSON-LD file. To do this:
    1. Uncomment [this line](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L60) and set `base_schema_org_file` to the name of the file you want to extend
    1. Uncomment [this line](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L65)
    1. If desired, edit [this line](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L172) to provide a new filename for export.


`data/original/` contains the original JSON files describing annotations, JSON-LD files
that extend the Biothings schema with our annotations, and JSON Schema files
derived from JSON-LD.

`data/jsonld-data-model/masterSage.jsonld` contains the output from running step 1 above on
`experimentalData.json` and `sageCommunity.json`.

Examples of functioning Schema.org schemas:
`data/jsonld-data-model/NFSchema.jsonld` (contains all NF related classes).


## Converting existing annotations to JSON Schemas directly

The `utilities/convert_to_json_schema.R` script converts all of our annotation
term definitions to JSON Schema. These can then be used as the building blocks
of a JSON Schema. Note that in order to retain information about the source and
description of each term, this script defines enumerated values as separate
`"const"` items rather than a simple enumerated list. Thus the resulting schemas
are somewhat more complex than will ultimately be necessary when this
information is captured in the schema.org source.

The `data/json-schemas-from-original/` subfolder has examples of schemas for
AMP-AD and NF that can serve as useful examples to guide development of
auto-generated schemas.

## Generating Schema.org schemas and JSONSchema schemas

To generate a Schema.org schema deriving directly from the Biothings Schema.org schema, please follow the usage examples below. 
Example cover augmenting Schema.org schemas with validation rules from which a JSONSchema schema can be generated, as well.

### Usage examples

schemaorg_req_example.py provides a self contained toy example of schema.org schema generation, along with example validation logic (e.g. required annotations, constrainining annotation input values, etc.)

Run 

```
python schemaorg_req_example.py 
```

to generate 
- example schema.org schema (schemas/exampleSchemaReq.jsonld)
- JSONSchema schema based on schema.org schema (schemas/exampleJSONSchema.json)
- annotations manifest based on the schema.org and JSONSchema schemas; NOTE: please read in-code comments and instructions regarding manifest generation and Google Sheet API credentials 

Both schemaorg_req_example.py and schema_generator.py are well documented; please refer to in-code documentation for more details. 


To validate sample data against the example schema:

```
ajv -s schemas/exampleJSONSchema.json -d 18889969.json --all-errors --errors=text
```

Examples of functioning Schema.org schemas augmented with validation rules: data/NFSchemaReq.jsonld (contains all NF related classes and associated validation rules).

See schemas/nf_jsonschema.json for a JSONSchema derived based on data/NFSchemaReq.jsonld. 
data/NFSchemaReq.jsonld was generated using nf_schema_add_requirements.py with input data/NFSchema.jsonld
schemas/nf_jsonschema.json was generated using schema_generator.py with input data/NFSchemaReq.jsonld
See in-code documentation for more details.

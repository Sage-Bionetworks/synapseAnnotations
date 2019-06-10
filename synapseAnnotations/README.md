# Generating Schema.org schemas and JSONSchema schemas

## Installation 

- clone this branch of the repo
- install dependencies (e.g. pip or conda; either should work):
  * networkx
  * rdflib
  * tabletext
  * urllib
  * graphviz (this is for visualization only)
  * jsonschema
  * orderedset

- we use ajv for testing example JSONSchemas; you can install via nodejs and npm

## Usage examples

schemaorg_req_example.py provides a self contained example of schema.org schema generation, along with example validation logic (e.g. required annotations, constrainining annotation input values, etc.)

Run 

```
python schemaorg_req_example.py 
```

to generate 
- example schema.org schema (schemas/exampleSchemaReq.jsonld)
- JSONSchema schema based on schema.org schema (schemas/exampleJSONSchema.json)

Both schemaorg_req_example.py and schema_generator.py are well documented; please refer to in-code documentation for more details. 


To validate sample data against the example schema:

```
ajv -s schemas/exampleJSONSchema.json -d 18889969.json --all-errors --errors=text
```

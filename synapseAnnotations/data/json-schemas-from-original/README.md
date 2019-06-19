# Schemas

Example schemas for AMP-AD and NF. They reference the definitions in the
`definitions/` folder. To check that the schemas are valid JSON Schema using
[ajv-cli](https://github.com/jessedc/ajv-cli):

```
ajv compile -s ampad_schema.json -r "definitions/*.json"
ajv compile -s nf_schema.json -r "definitions/*.json"
```

To validate sample data against the AMP-AD schema:

```
ajv -s ampad_schema.json -r "definitions/*.json" -d ampad_demo.json
```

To validate data and show all errors at once: 

```
ajv -s ampad_schema.json -r "definitions/*.json" -d ampad_demo.json --all-errors
```

To view more human readable results:

```
ajv -s ampad_schema.json -r "definitions/*.json" -d ampad_demo.json --all-errors --errors=text
```

Save results to a file (note that if there are too many errors, ajv-cli
truncates the output and I have not yet found a way to get all of it; it will
also be truncated in the resulting file):

```
ajv -s ampad_schema.json -r "definitions/*.json" -d result.json --all-errors 2> output.json
```

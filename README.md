# Synapse Annotations Schemas

Sage Bionetworks derived standards for annotating content in Synapse. This
provide a mechanism for defining, managing, and implementing controlled
vocabularies when annotating content in Synapse. 

## What's here

There are schemas for individual terms in the `terms/` folder. The terms are
organized into modules. There are subfolders for each module, and the term names
include the module (e.g. `experimentalData.assay`). The terms are mini schemas
that are valid JSON Schema, such as the following:

```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "sage.annotations-experimentalData.specimenID-0.0.1",
    "description": "Identifying string linked to a particular sample or specimen",
    "type": "string"
}
```

Templates for adding new terms are included in the `term-templates/` folder.

To register these schemas in Synapse use the `register-schemas.R` script. To
register all schemas in the repo, run:

```
./register-schemas.R terms/*/*.json
```

Note that this will show failures for schemas that have already been registered.
You can learn more about how to use this script by running:

```
./register-schemas.R --help
```

Each project can use these terms to build a schema or set of schemas to validate
annotations. By referencing the terms that are registered in Synapse, we can
reuse the same vocabulary while allowing each project to set requirements based
on their own needs. An example of such a schema is at `schemas/testschema.json`.
This too has been registered in Synapse. Real project schemas for AMP-AD, PEC,
HTAN, NF, etc. could live in this repo or could be stored elsewhere. Either way,
they'll reference the terms defined here.

Building schemas this way also provides some very limited support for synonyms.
A schema that reuses the values for `fileFormat` but wants to call the key
`fileType` could do so as follows (though we encourage using the same key names
whenever possible, since queries on Synapse will still treat `fileFormat` and
`fileType` as two unrelated keys):

```
"fileType": {
    "$ref": "sage.annotations-sageCommunity.fileFormat-0.0.1"
}
```

The `bind-schema.R` shows an example of how to bind `testschema.json` to a
folder, and validate annotations against it. This is just for demonstration
purposes.

## What's to come

To use these terms, HTAN and other projects that use
[schematic](https://github.com/sage-bionetworks/schematic): schematic will soon 
support exporting terms from json-ld data models to JSON schema objects in the format 
required here. Once exported, these objects can be committed to the Synapse annotations 
vocabulary following the standard term submission process outlined here. 
We are working hard on documenting the export feature in schematic and will link 
to it here when ready.


Over time we will add terms to the vocabulary, and change existing terms. The
terms are versioned, and each time a term is changed we will update the version
number. That means that only the most recent version will appear in the GitHub
repo, but older versions will remain registered in Synapse. We may want to
consider building a tool that makes it easier to look up older versions of a
term. Schemas can continue to reference old versions of a term. If a project
wants to redefine a term, it can create its own term in its own organization and
reference that one instead.

We'd like to automatically register updated terms to Synapse (likely also via a
GitHub Actions workflow that runs upon merging to the main branch). In the past,
there was a cumbersome release process for the synapseAnnotations repo that
caused long delays between when terms were approved and when they were available
in downstream tools. Automatically registering terms will ensure that once
they've been agreed upon, they're immediate available for use.

## Remaining questions

A few questions remain:

- Compiling schemas locally: validation libraries like ajv let you check that
  JSON Schema is valid according to the JSON Schema spec, however this does not
  work for `testschema.json`. That's because referencing terms in a way that
  Synapse understands (in the format `organization-schema.name-version.number`)
  makes it impossible for a local validator to find them. I'm not sure what we
  should do about this.

## TODO:

- [X] Convert JSON Schema files into individual mini-schemas (under `terms/`)
- [X] Validate mini-schemas with `ajv compile`
- [X] Convert format to Synapse's required format (with `"concreteType"`)
- [X] Register these mini-schemas on Synapse and ensure they work
- [X] Build a more complete schema that references the mini-schemas
- [X] Register that schema and ensure that it works
- [X] Add templates for new terms to make contributing easier
- [X] Bind schema to an entity and test validation
- [X] Set up CI to check that mini-schemas are valid. Need to also ensure that
      the version number is incremented if the schema changes.
- [ ] Automatically register terms in Synapse

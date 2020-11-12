# README

A possible way to organize vocabularies going forward. The goal here is to have
a common set of terms we can reuse across schemas. Individual projects could
reference those terms when building schemas, because the terms themselves would
be registered in Synapse.

## What's here

There are schemas for individual terms in the `terms/` folder. The terms are
organized to mirror the modules in the original synapseAnnotations repo: there
are subfolders for each module, and the term names include the module (e.g.
`experimentalData.assay`). The terms are mini schemas that are valid JSON
Schema, such as the following:

```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "karatestorg20201105-experimentalData.specimenID-0.0.1",
    "description": "Identifying string linked to a particular sample or specimen",
    "type": "string"
}
```

Templates for adding new terms are included in the `term-templates/` folder.

To register these schemas in Synapse `register-schemas.R`.

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
    "$ref": "karatestorg20201105-sageCommunity.fileFormat-0.0.1"
}
```

The `bind-schema.R` shows an example of how to bind `testschema.json` to a
folder, and validate annotations against it. This is just for demonstration
purposes.

## What's to come

To use these terms, HTAN and other projects that use
[schematic](https://github.com/sage-bionetworks/schematic) will need to generate...
[milen can you fill this in?]

Over time we will add terms to the vocabulary, and change existing terms. The
terms are versioned, and each time a term is changed we will update the version
number. That means taht only the most recent version will appear in the GitHub
repo, but older versions will remain registered in Synapse. We may want to
consider building a tool that makes it easier to look up older versions of a
term. Schemas can continue to reference old versions of a term. If a project
wants to redefine a term, it can create its own term in its own organization and
reference that one instead. 

Because versioned schemas are immutable, it is important that we always
increment the version when we change a schema. We will want to add testing to
this repo that can compare an updated version of a file with the previous
version and ensure that the version number has changed if the schema changed.
Ideally these tests will run on GitHub Actions or similar to ensure that
proposed changes follow the versioning rules before being merged. We should also
test that the terms themselves are valid JSON schema.

This testing will be important because we'd like to automatically register
updated terms to Synapse (likely also via a GitHub Actions workflow that runs
upon merging to the main branch). In the past, there was a cumbersome release
process for the synapseAnnotations repo that caused long delays between when
terms were approved and when they were available in downstream tools.
Automatically registering terms will ensure that once they've been agreed upon,
they're immediate available for use.

If we agree on this approach, then the contents of this repo should be moved to
the synapseAnnotations repo.

## Remaining questions

A few questions remain:

- Compiling schemas locally: validation libraries like ajv let you check that
  JSON Schema is valid according to the JSON Schema spec, however this does not
  work for `testschema.json`. That's because referencing terms in a way that
  Synapse understands (in the format `organization-schema.name-version.number`)
  makes it impossible for a local validator to find them. I'm not sure what we
  should do about this.
- How do we set up the testing and CI described above? (Kara is working on this
  and has some ideas, but nothing in place and working yet)
  - One potential issue I'm writing here so I don't forget: if we want to
    register schemas on merge, we should have the PR attempt to register them as
    well so we can catch any issues before merging. The PR should either
    register them to a different organization (tricky since the organization
    name is in the schema itself), or to the Synapse staging endpoint instead of
    prod. But imagine this: Jane opens a PR that adds a new value for `assay`,
    and she increments the version number. Anya reviews the PR and asks that
    Jane include a description for her new assay. Jane makes the change and
    pushes to her branch. There's no need to increment the version a second time
    since the prod version of the schema hasn't changed yet, but we also can't
    re-register it on staging because the version from Jane's first commit was
    already registered. Maybe when registering on staging we want to append the
    commit sha to the version number to ensure uniqueness (*need to find out if
    Synapse schema versioning would support this*). We probably would *not* want
    to do this for the final schemas: that would make it very hard for people to
    find which version to reference, since it wouldn't be tracked in the GitHub
    versions of the schemas themselves.
    - John noted that a better approach, instead of registering schemas on
      staging, might be to have a way for Synapse to tell us if a schema would
      be valid without actually registering it. That should allow us to skip
      adding the commit sha to a version.

## TODO:

- [X] Convert JSON Schema files into individual mini-schemas (under `terms/`)
- [X] Validate mini-schemas with `ajv compile`
- [X] Convert format to Synapse's required format (with `"concreteType"`)
- [X] Register these mini-schemas on Synapse and ensure they work
- [X] Build a more complete schema that references the mini-schemas
- [X] Register that schema and ensure that it works
- [X] Add templates for new terms to make contributing easier
- [X] Bind schema to an entity and test validation
- [ ] Set up CI to check that mini-schemas are valid. Need to also ensure that
      the version number is incremented if the schema changes.
- [ ] Automatically register terms in Synapse

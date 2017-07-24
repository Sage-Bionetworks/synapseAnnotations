[![Build Status](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations.svg?branch=master)](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations)

# Introduction

Sage Bionetworks derived standards for annotating content in Synapse.

# Schemas

Schemas are stored here in [Synapse Table Schema](http://docs.synapse.org/articles/tables.html) format. A schema is a list of [`Column Model`s](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnModel.html) in JSON format.

Column types are required, and the valid types can be found [here](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnType.html).

# Development

Internal development can be performed by branching from `master` to your own feature branch, making changes, pushing the branch to this repository, and opening a pull request. Pull requests against the master branch require a review before merging.

All pushed branches and pull requests are also tested through the continuous integration service [Travis CI](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations). All JSON files are linted using [demjson's](deron.meranda.us/python/demjson/) `jsonlint` command line program.

When modifying the JSON schema files, we encourage you to install `demjson` to test your JSON files:

```
pip install demjson==2.2.4
```

or use the provided [requirements.txt](requirements.txt) file provided in this repository:

```
pip install -r requirements.txt
```
# Release Versioning Annotations  
synapseAnnotations release version tags structure **v0.0.0** fits within [semantic versioning](http://semver.org/) guidelines. 
The tags release numbering scheme is defined as: 

Major version **v0** increments by:
1. Changes in data structure (ex. yaml to json or json to mongodb)
2. Changes in keys 
3. Changes in values 

Minor version **.0.** increments by: 
1. Adding keys
2. Adding values 

Patch version **.0** increments by: 
1. Errors that don't break the API 

To optimize usability, the release tags will be placed on 2 required and 1 optional locations: 
1. A Synapse project's entity annotation as a single value vs. list of versions and defined by the key **annotationVersion** uniformly through synapse projects. 
2. [Annotation UI](https://github.com/Sage-Bionetworks/annotationUI) **title** 
3. OPTIONAL: **Project's wiki** 

**Note:** _Git Commit messages including the words **added** or **changed** would facilitate the release version incrementation process_ 



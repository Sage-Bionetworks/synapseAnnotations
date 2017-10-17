[![Build Status](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations.svg?branch=master)](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations)

# Introduction

Sage Bionetworks derived standards for annotating content in Synapse.

# Schemas

Schemas are stored here in [Synapse Table Schema](http://docs.synapse.org/articles/tables.html) format. A schema is a list of [`Column Model`s](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnModel.html) in JSON format.

Column types are required, and the valid types can be found [here](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnType.html).

# Development

Internal development can be performed by branching from `develop` to your own feature branch, making changes, pushing the branch to this repository, and opening a pull request. Pull requests against the `develop` branch require a review before merging. The only pull requests that will go to `master` are from `develop`, and will trigger a new release (see below for release procedures). If you are editing using the Github web site, make sure you switch to the `develop` branch first before clicking the `Edit this file` button. If you accidentally open a pull request against `master`, you can change this in your pull request using the `Edit` button.

All pushed branches and pull requests are also tested through the continuous integration service [Travis CI](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations). All JSON files are linted using [demjson's](deron.meranda.us/python/demjson/) `jsonlint` command line program.

When modifying the JSON schema files, we encourage you to install `demjson` to test your JSON files:

```
pip install demjson==2.2.4
```

or use the provided [requirements.txt](requirements.txt) file provided in this repository:

```
pip install -r requirements.txt
```

## Proposing changes

1. Make changes on your feature branch.
1. Request and complete a review from someone on the team.
1. When review is completed, note it to be reviewed and merged at the weekly meeting.
1. Finalize merge into the `master` branch.
1. Update the version and make a versioned release (with assistance from @teslajoy)

# Release Versioning Annotations
Releases are made through Github tags and are available on the [Releases](https://github.com/Sage-Bionetworks/synapseAnnotations/releases) page.

The release version structure **v0.0.0** follows [semantic versioning](http://semver.org/) guidelines. New releases are made using the following rules:

Major version **v0** increments by:
1. Changes in data structure (ex. yaml to json or json to mongodb)
2. Changes to existing keys
3. Changes to existing values

Minor version **.0.** increments by: 
1. Adding keys
2. Adding values

Patch version **.0** increments by: 
1. Errors or corrections that don't break the API

To optimize usability, the release tags should be placed on two required and one optional locations: 
1. A Synapse Project annotation as a single value vs. list of versions and defined by the key **`annotationVersion`**. 
2. The Shiny application [Annotation UI](https://github.com/Sage-Bionetworks/annotationUI)'s **title** 
3. OPTIONAL: Documented in a Synapse Project wiki.

**Note:** _Git Commit messages including the words **added** or **changed** would facilitate the release version incrementation process_ 

## Update `CHANGELOG.md` and release notes

After drafting a release, use this [Ruby package](https://github.com/skywinder/github-changelog-generator) to autogenerate a `CHANGELOG.md` locally that can be committed to the repository. It requires a Github Personal Access Token.

```



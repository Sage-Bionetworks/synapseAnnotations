[![Build Status](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations.svg?branch=master)](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations)

> Use our [Annotation UI](shiny.synapse.org/users/nsanati/annotationUI/) application to easily view and search our existing annotation definitions:
>

# Introduction

Sage Bionetworks derived standards for annotating content in Synapse. This provide a mechanism for defining, managing, and implementing controlled vocabularies when annotating content in Synapse. The standards here are developed for Sage Bionetworks supported communities and consortiums by the [Sage Bionetworks Synapse Annotations working group](https://www.synapse.org/annotation) but are available for any other use.

# Annotation definitions

This repository contains schemas that define the things we want to annotate as well as the controlled values that may be used. You can think of these as 'columns' of a table, each with a limited set of values that can occur in each column.

Our schema definitions are stored here in [Synapse Table Schema](http://docs.synapse.org/articles/tables.html) format. A schema is a list of [`Column Model`s](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnModel.html) in JSON format. Using this format allows us to use them in a straightforward manner with other features of Synapse, including [file views](http://docs.synapse.org/articles/fileviews.html) and [tables](http://docs.synapse.org/articles/tables.html).

Column types are required, and the valid types can be found [here](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnType.html).

# Organization

All schema definitions can be found in the [synapseAnnotations/synapseAnnotations/data/](synapseAnnotations/synapseAnnotations/data/) folder. There are three high level schemas: [experimental data](synapseAnnotations/synapseAnnotations/data/experimentalData.json), [tool](synapseAnnotations/synapseAnnotations/data/tool.json), and [analysis](synapseAnnotations/synapseAnnotations/data/analysis.json).

Schemas for specific communities and consortia are also defined, such as for the [neurodegenerative diseases consortiums](synapseAnnotations/data/neuro.json), [cancer consortiums](synapseAnnotations/data/cancer.json), and specific group such as (but not limited to) [Project GENIE](synapseAnnotations/data/genie.json).

# Development

This section discusses the technical steps for developing on this repository. See the [CONTRIBUTING.md](CONTRIBUTING.md) document for more information on how to contribute annotations to this project.

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
1. Finalize merge into the `develop` branch.
1. Update the version and make a versioned release (with assistance from @teslajoy)

# Release Versioning Annotations
Releases are made through Github tags and are available on the [Releases](https://github.com/Sage-Bionetworks/synapseAnnotations/releases) page.

The release version structure **vX.X.X** follows [semantic versioning](http://semver.org/) guidelines. New releases are made using the following rules:

Major version increments by:
1. Changes in data structure (ex. yaml to json or json to mongodb)
2. Changes to existing keys
3. Changes to existing values

Minor version increments by:
1. Adding keys
2. Adding values

Patch version increments by:
1. Errors or corrections that don't break the API

To optimize usability, the release tags should be placed on two required and one optional locations:
1. A Synapse Project annotation as a single value defined by the key **`annotationReleaseVersion`**.
2. The Shiny application [Annotation UI](https://github.com/Sage-Bionetworks/annotationUI)'s **title**
3. OPTIONAL: Documented in a Synapse Project wiki.

## Update `CHANGELOG.md` and release notes

After drafting a release, use this [Ruby package](https://github.com/skywinder/github-changelog-generator) to auto-generate a `CHANGELOG.md` locally that can be committed to the repository. It requires a [Github Personal Access Token](https://github.com/settings/tokens).

```

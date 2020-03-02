[![Build Status](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations.svg?branch=master)](https://travis-ci.org/Sage-Bionetworks/synapseAnnotations)

> Use our [Annotation UI](https://shiny.synapse.org/users/nsanati/annotationUI/) application to easily view and search our existing annotation definitions:
>

# Introduction

Sage Bionetworks derived standards for annotating content in Synapse. This provide a mechanism for defining, managing, and implementing controlled vocabularies when annotating content in Synapse. The standards here are developed for Sage Bionetworks supported communities and consortiums by the [Sage Bionetworks Synapse Annotations working group](https://www.synapse.org/annotation) but are available for any other use.

# Annotation definitions

This repository contains schemas that define the things we want to annotate as well as the controlled values that may be used. You can think of these as 'columns' of a table, each with a limited set of values that can occur in each column.

Our schema definitions are stored here in [Synapse Table Schema](http://docs.synapse.org/articles/tables.html) format. A schema is a list of [`Column Model`s](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnModel.html) in JSON format. Using this format allows us to use them in a straightforward manner with other features of Synapse, including [file views](http://docs.synapse.org/articles/fileviews.html) and [tables](http://docs.synapse.org/articles/tables.html).

Column types are required, and the valid types can be found [here](http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/ColumnType.html).

# Organization

All schema definitions can be found in the [synapseAnnotations/data/](synapseAnnotations/data/) folder. There are three high level schemas: [experimental data](synapseAnnotations/data/experimentalData.json), [tool](synapseAnnotations/data/tool.json), and [analysis](synapseAnnotations/data/analysis.json).

Schemas for specific communities and consortia are also defined, such as for the [neurodegenerative diseases consortiums](synapseAnnotations/data/neuro.json), [cancer consortiums](synapseAnnotations/data/cancer.json), and specific group such as (but not limited to) [Project GENIE](synapseAnnotations/data/genie.json).

# Development

This section discusses the steps for developing on this repository. See the [CONTRIBUTING.md](CONTRIBUTING.md) document for more information on how to contribute annotations to this project.

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
1. The Shiny application [Annotation UI](https://github.com/Sage-Bionetworks/annotationUI)'s **title**
1. OPTIONAL: Documented in a Synapse Project wiki.

## Update `CHANGELOG.md` and release notes

After drafting a release, use this [Ruby package](https://github.com/skywinder/github-changelog-generator) to auto-generate a `CHANGELOG.md` locally that can be committed to the repository. It requires a [Github Personal Access Token](https://github.com/settings/tokens). The token should have all `repo` scope permissions. Generate a key and save the string that GitHub provides as an env variable in bash: `export CHANGELOG_GITHUB_TOKEN=<your_token_here>`.

The steps to create a release are as follows:

1. Merge the develop branch into master and push to GitHub
1. Run the [changelog generator](https://github.com/github-changelog-generator/github-changelog-generator)
   1. If you haven't already, install the changelog generator `gem install github_changelog_generator`
   1. From within the synapseAnnotations directory on your machine, run `github_changelog_generator -u Sage-Bionetworks -p synapseAnnotations --future-release X.X.X` (replacing `X.X.X` with the new version number)
1. Commit the new CHANGELOG.md directly to master and push to GitHub.
1. Create a new release on Github using the web interface. Both the tag version and release title should be "vX.X.X".
1. Copy the new section of CHANGELOG.md to release notes section of the new release.
1. Merge the master branch into develop and push to GitHub.

Generally, you will next want to update the [Synapse table](https://www.synapse.org/#!Synapse:syn10242922) that describes the annotations and powers the [AnnotationUI](https://shinypro.synapse.org/users/nsanati/annotationUI/):

1. Run the script `update_annotations_table.R`

Additional information about the release process can be found in [issue 392](https://github.com/Sage-Bionetworks/synapseAnnotations/issues/392)

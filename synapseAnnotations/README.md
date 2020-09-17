# Synapse Annotations data models and scripts

This folder contains data and scripts to manage our annotations data models.

## Install necessary packages

Install [schematic](https://github.com/Sage-Bionetworks/schematic/tree/main). schematic provides tools to create, manage, and 
use schemas; it is compatible with Synapse.

## Convert previous annotations to current format

The `sage_annotations_2_csv_schema.py` script converts the previous annotations
format to the CSV file `sage_controlled_vocabulary_schema.csv`. It operates on
data files in `data/original-json` and should not need to be run again, but is
here for posterity. 

Going forward, changes should be made to the
`sage_controlled_vocabulary_schema.csv` file directly.

The `Attribute` column contains both keys and values, which are matched to one
another via the `Parent` column. For example, `rnaSeq` is a value for key
`assay`, and therefore has `assay` in the `Parent` column. The `Description` and
`Source` columns give additional information about the term. `Valid Values`
gives a list of the valid values for that term; if blank or `"children"`, then
all rows that have that term as their parent are considered valid values. The
`Requires` column indicates conditional dependencies; if the current term is
present, it requires these additional terms.

## Convert CSV to JSON-LD

Run `python sage_schema.py` to convert `sage_controlled_vocabulary_schema.csv`
to JSON-LD. `example_schema.py` is basically the same, but for the example CSV
in the `schemas/` subfolder.

## Generate a manifest

Run `python example_schema_usage.py`. Requires access to a Google API
credentials file stored on Synapse.

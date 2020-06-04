# Synapse Annotations data models and scripts

This folder contains data and scripts to manage our annotations data models.

## Install necessary packages

```
pip install -r requirements.txt
```

## Convert previous annotations to current format

The `sage_annotations_2_csv_schema.py` script converts the previous annotations
format to the CSV file `sage_controlled_vocabulary_schema.csv`. It operates on
data files in `data/original-json` and should not need to be run again, but is
here for posterity. 

Going forward, changes should be made to the
`sage_controlled_vocabulary_schema.csv` file directly.

## Convert CSV to JSON-LD

Run `python sage_schema.py` to convert `sage_controlled_vocabulary_schema.csv`
to JSON-LD. `example_schema.py` is basically the same, but for the example CSV
in the `schemas/` subfolder.

## Generate a manifest

Run `python example_schema_usage.py`. Requires access to a Google API
credentials file stored on Synapse.

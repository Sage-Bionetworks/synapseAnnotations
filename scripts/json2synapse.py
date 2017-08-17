import os
import requests
import json
import argparse
import pandas
import synapseclient
from synapseclient import Table

syn = synapseclient.login()


def json2flatten(path, module):
    """fetch and read raw json objects from its' github url path and decode the json object to its raw format"""
    json_record = pandas.read_json(path)

    # grab annotations with empty enumValue lists i.e. don't require normalization and structure their schema
    empty_vals = json_record.loc[json_record.enumValues.str.len() == 0]
    empty_vals = empty_vals.drop('enumValues', axis=1)
    empty_vals['valueDescription'] = ""
    empty_vals['source'] = ""
    empty_vals['value'] = ""
    empty_vals['module'] = module

    empty_vals.set_index(empty_vals['name'], inplace=True)

    # for each value list object
    flatten_vals = []
    json_record = json_record.loc[json_record.enumValues.str.len() > 0]
    json_record.reset_index(inplace=True)

    for i, jsn in enumerate(json_record['enumValues']):
        normalized_values_df = pandas.io.json.json_normalize(jsn)

        # re-name 'description' defined in dictionary to valuesDescription to match table on synapse schema
        normalized_values_df = normalized_values_df.rename(columns={'description': 'valuesDescription'})

        # grab key information in its row, expand it by values dimension and append its key-columns to flattened values
        rows = json_record.loc[[i], json_record.columns != 'enumValues']
        repeats = pandas.concat([rows] * len(normalized_values_df.index))
        repeats.set_index(normalized_values_df.index, inplace=True)
        flatten_df = pandas.concat([repeats, normalized_values_df], axis=1)
        # add column module for annotating the annotations
        flatten_df['module'] = module
        flatten_df.set_index(flatten_df['name'], inplace=True)

        flatten_vals.append(flatten_df)

    flatten_vals.append(empty_vals)
    module_df = pandas.concat(flatten_vals)
    module_df = module_df.rename(columns={'name': 'key'})

    return module_df


def updateTable(tableSynId, newTable, releaseVersion):
    """
    Gets the current annotation table, deletes all it's rows, then updates the table with new content generated
    from all the json files on synapseAnnotations. In the process also updates the table annotation to the latest release version.
    """

    currentTable = syn.tableQuery("SELECT * FROM %s" % tableSynId)

    # If current table has rows, delete all the rows of them
    if currentTable.asRowSet().rows:
        deletedRows = syn.delete(currentTable.asRowSet())

    # get table schema and set it's release version annotation
    schema = syn.get(tableSynId)
    schema.annotations = {"releaseVersion": str(releaseVersion)}
    updated_schema_release = syn.store(schema)

    # store the new table on synapse
    table = syn.store(Table(schema, newTable))


def main():
    """
    Given a synapse table id with the schema
        annotation_schema = ["key", "description", "columnType", "maximumSize", "value", "valuesDescription",
                         "source", "module"]
    get the most updated release version annotations json files from github Sage-Bionetworks/synapseAnnotations
    normalize the json files per module and create a melted data frame by concatenating all the modules data.
    then upload the melted data frame to the synapse table by completely deleting all rows then replacing content.
    This process also updates the synapse table annotations with the latest release version.


    This code was built under
    Python 2.7.13 :: Anaconda 4.4.0 (x86_64)
    pandas 0.19.2

    Example run:
        python scripts/json2synapse.py --tableId  syn1234 --releaseVersion 'v2.1.1'
    """
    parser = argparse.ArgumentParser('Creates a flattened synapse table from json files located on '
                                     'Sage-Bionetworks/synapseAnnotations/data.')
    parser.add_argument('--tableId', help='A table synapse id containing the annotations',
                        required=False, type=str)
    parser.add_argument('--releaseVersion', help='Sage-Bionetworks/synapseAnnotations release version tag name',
                        required=False, type=str)

    # assign tableSynId from user-input if it exists
    args = parser.parse_args()
    if args.tableId is not None:
        tableSynId = args.tableId
    else:
        tableSynId = "syn10242922"

    if args.releaseVersion is not None:
        releaseVersion = args.releaseVersion
    else:
        # get the latest release version
        reqRelease = requests.get("https://api.github.com/repos/Sage-Bionetworks/synapseAnnotations/releases")
        releaseVersion = reqRelease.json()[0]['tag_name']

    all_modules = []
    key = ["key", "value", "module"]
    annotation_schema = ["key", "description", "columnType", "maximumSize", "value", "valuesDescription",
                         "source", "module"]

    # get and load the list of json files from data folder (given the api endpoint url - ref master - latest vesion)
    # then construct a dictionary of module names and its associated raw data github url endpoints.
    # example {u'analysis':
    #          u'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/analysis.json',
    #          ... } @kenny++
    # there is code for fetching a specific release version if needed in future.
    # https://github.com/teslajoy/synapseRAUtils/blob/master/githubfiles.py
    req = requests.get(
        'https://api.github.com/repos/Sage-Bionetworks/synapseAnnotations/contents/synapseAnnotations/data/?ref=master')
    file_list = json.loads(req.content)
    names = {os.path.splitext(x['name'])[0]: x['download_url'] for x in file_list}

    for module, path in names.iteritems():
        module_df = json2flatten(path, module)
        all_modules.append(module_df)

    # concat the list of all normalized dataframes into one annotation dataframe
    all_modules_df = pandas.concat(all_modules)

    # re-arrange columns/fields and sort data.
    # this step is important for testing (compare_key_values()) where we diff two data frames
    all_modules_df = all_modules_df[annotation_schema]
    all_modules_df.sort_values(key, ascending=[True, True, True], inplace=True)

    # To resolve an error from global searching inside annotationUI R shiny app data tables (https://datatables.net/)
    # I had to convert data encoding here. Currently this issue seems to be resolved, but leaving code in
    # in case of failure. It could also help for testing or creating a table via csv upload
    # to print out the modules data.
    # all_modules_df.to_csv("annot.csv", sep=',', index=False, encoding="utf-8")
    # all_modules_df = pandas.read_csv('annot.csv', delimiter=',', encoding="utf-8")
    # os.remove("annot.csv")

    updateTable(tableSynId=tableSynId, newTable=all_modules_df, releaseVersion=releaseVersion)


if '__main__' == __name__:
    main()

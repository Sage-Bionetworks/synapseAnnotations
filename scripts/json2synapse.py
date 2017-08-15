import os
import sys
import requests
import json
import logging
import argparse
import pandas
import numpy
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


def rightJoin(df1, df2, key, suffixes):
    """Identify rows in df2 that are not in df1 based on unique keys ["key", "value", "module"] (can be a list: one-to many args).
       After merging the two data frames, columns will be added with suffixes append to it's columns (not defined as key)"""
    df3 = pandas.merge(df1, df2, on=key, how='right', indicator='Exist', suffixes=suffixes)
    df3['Exist'] = numpy.where(df3.Exist == 'both', True, False)
    return df3


def outerJoin(df1, df2):
    """ Identify rows in df1 that are not in df2 and return then as a data frame"""
    df3 = pandas.merge(df1, df2, how='outer', indicator=True).query('_merge == "left_only"').drop(['_merge'], axis=1)
    return df3


def updateTable(tableSynId, newTable, key, delta=False, whereClause=False):
    """
    A table may have one-many key(s) in a table schema predefined by the user
    There are three cases where changes can be done to a table:

        Case 1: The unique keys have been changed but the remaining schema values are the same
        Case 2: The schema values have been changed but the keys are the same
        Case 3: New rows that have been added to table

    :param tableSynId: the synapse table Id
    :param newTable: synapseAnnotations normalized and melted json files into a new dataframe
    :param key: the unique identifiers of the schema in our case the tuple (key-value)
    :param delta: if previous version of changes should not be deleted
    :param whereClause: synapse table query where clause that follows a SQL language syntax
    :return: None and table on synapse identified by tableSynId should be updated
    """

    currentTable = syn.tableQuery("SELECT * FROM %s" % tableSynId)
    currentTable = currentTable.asDataFrame()

    if sum(pandas.Series(key).isin(currentTable.columns)) == 0:
        sys.exit("None of the unique keys (key | value | module) exists in this tables schema. "
                 "Please add the columns key,  value, and module to your table.")
    elif sum(pandas.Series(key).isin(currentTable.columns)) == 1:
        sys.exit("One of the unique keys columns (key | value | module) doesn't exist. Please make sure "
                 "that the columns key | value | module exists in your table.")
    else:
        logging.info("Unique keys key | value | module exists in schema and pursuing")

    # Test cases: change a non-key column cell (valuesDescription) and change a unique key cell (value)
    # newTable.iloc[3, newTable.columns.get_loc('valuesDescription')] = 'exome sequencing Nasim'
    # newTable.iloc[1, newTable.columns.get_loc('value')] = 'Nasim'

    # standardize na/NAN in data by replacing it with an empty string for match comparisons
    currentTable = currentTable.fillna("")
    newTable = newTable.fillna("")

    # Match schema in current and new tables
    schema = currentTable.columns
    newTable = newTable[currentTable.columns]

    # Keep row id/version that a row index (this is due to merge procedures)
    currentTable['index'] = currentTable.index

    ## Case 1: find the rows where the unique keys have been changed but the remaining schema values are the same
    resultDF = rightJoin(df1=currentTable, df2=newTable, key=key, suffixes=('_cur', '_new'))

    newCol = key + [s + '_new' for s in [col for col in newTable.columns if col not in key]]
    changedRows = resultDF.loc[resultDF.Exist == False, newCol].drop_duplicates()

    newCol = [c.replace('_new', '') for c in newCol]
    changedRows.columns = newCol

    # column names in schema and not in keys
    notKey = [col for col in newTable.columns if col not in key]
    # standardize na/NAN in data by replacing it with an empty string for match comparisons
    changedRows = changedRows.fillna("")

    changedKeys = rightJoin(df1=changedRows, df2=currentTable, key=notKey, suffixes=('_new', '_cur'))

    changedKeys.columns = [c.replace('_cur', '') for c in changedKeys.columns]
    changedKeysRows = changedKeys.loc[changedKeys.Exist == True, currentTable.columns]

    ## Case 2: The schema values has changed but the keys are the same
    currentUpdated = outerJoin(currentTable, newTable)
    # only grab the rows with changed schema values and not changed keys
    changedSchemaValues = outerJoin(currentUpdated, changedKeysRows)

    ##  Case 1 or 2: Remove changed rows in current table
    if not changedSchemaValues.empty or not changedKeysRows.empty:

        if not changedSchemaValues.empty and changedKeysRows.empty:
            logging.info("Deleting rows with updated schema values")
            changedSchemaValues.set_index('index', inplace=True, drop=True)
            toDelete = changedSchemaValues
            deleteRows = syn.delete(Table(syn.get(tableSynId), toDelete))

        if not changedKeysRows.empty and changedSchemaValues.empty:
            logging.info("Deleting rows with updated keys")
            changedKeysRows.set_index('index', inplace=True, drop=True)
            toDelete = changedKeysRows
            deleteRows = syn.delete(Table(syn.get(tableSynId), toDelete))

        if not changedSchemaValues.empty and not changedKeysRows.empty:
            logging.info("Deleting rows with updated keys and schema values")
            changedSchemaValues.set_index('index', inplace=True, drop=True)
            changedKeysRows.set_index('index', inplace=True, drop=True)
            toDelete = pandas.concat([changedKeysRows, changedSchemaValues])
            deleteRows = syn.delete(Table(syn.get(tableSynId), toDelete))

        else:
            logging.info("No rows to delete in current table")

    # Case 1,2,3: All new or updated rows to be added to table
    newOrUpdated = outerJoin(newTable, currentTable)
    newOrUpdated = newOrUpdated[schema]
    newOrUpdated.sort_values(['key', 'value', 'module'], ascending=[True, True, True], inplace=True)
    if not newOrUpdated.empty:
        logging.info("Storing new and updated changes")
        table = syn.store(Table(syn.get(tableSynId), newOrUpdated))


def main():
    """
    Given a synapse table is with the schema
        annotation_schema = ["key", "description", "columnType", "maximumSize", "value", "valuesDescription",
                         "source", "module"]
    get the most updated release version annotations json files from github Sage-Bionetworks/synapseAnnotations
    normalize the json files per module and create a melted data frame by concatenating all the modules data.
    then upload the melted data frame to the synapse table and update the tables content by checking for rows
    that have been changed.

    This code was built under
    Python 2.7.13 :: Anaconda 4.4.0 (x86_64)
    pandas 0.19.2

    Here is a link to pandas documentation on merge, join, and concatenation of data frames pandas
    documentation on https://pandas.pydata.org/pandas-docs/stable/merging.html

    Example run:
        python scripts/json2synapse.py --tableId  syn1234
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--tableId', help='A table synapse id containing the annotations',
                        required=False, type=str)

    # assign tableSynId from user-input if it exists
    args = parser.parse_args()
    if args.tableId is not None:
        tableSynId = args.tableId
    else:
        tableSynId = "syn10242922"

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

    updateTable(tableSynId=tableSynId, newTable=all_modules_df, key=key, delta=False, whereClause=False)


if '__main__' == __name__:
    main()

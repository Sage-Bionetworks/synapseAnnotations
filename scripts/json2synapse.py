import os
import sys
import pandas
import numpy
import synapseclient
from synapseclient import Table
from pandas.io.json import json_normalize
import logging

syn = synapseclient.login()

# TODO: replace with auto download of raw files in repo
analysis = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/analysis.json'
sageCommunity = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/sageCommunity.json'
array = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/array.json'
cancer = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/cancer.json'
dhart = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/dhart.json'
experimentalData = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/experimentalData.json'
genie = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/genie.json'
neuro = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/neuro.json'
neurofibromatosis = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/neurofibromatosis.json'
ngs = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/ngs.json'
tool = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/tool.json'
toolExtended = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/toolExtended.json'

paths = [analysis, sageCommunity, array, cancer, dhart, experimentalData, genie, neuro, neurofibromatosis, ngs, tool, toolExtended]
names = ['analysis', 'sageCommunity', 'array', 'cancer', 'dhart', 'experimentalData', 'genie', 'neuro', 'neurofibromatosis', 'ngs', 'tool', 'toolExtended']


all_modules = []

tableSynId = "syn10242922"
key = ["key", "value"]


def json2flatten(path, module):
    # fetch and read raw json objects from its' github url and decode the json object to its raw format
    json_record = pandas.read_json(path)

    # grab annotations with empty enumValue lists i.e. don't require normalization and structure their schema
    empty_vals = json_record.loc[json_record.enumValues.str.len() == 0]
    empty_vals = empty_vals.drop('enumValues', axis=1)

    empty_vals['enumValues_description'] = ""
    empty_vals['enumValues_source'] = ""
    empty_vals['enumValues_value'] = ""
    empty_vals['module'] = module

    empty_vals.set_index(empty_vals['name'], inplace=True)

    # for each value list object
    flatten_vals = []
    json_record = json_record.loc[json_record.enumValues.str.len() > 0]
    json_record.reset_index(inplace=True)

    for i, jsn in enumerate(json_record['enumValues']):
        df = pandas.io.json.json_normalize(json_record['enumValues'][i])
        # re-name columns to match table on synapse schema
        df = df.rename(columns={'value': 'enumValues_value', 'description': 'enumValues_description',
                                'source': 'enumValues_source'})

        # grab key information in its row, expand it by values dimention and append its key-columns to flattened values
        rows = json_record.loc[i:i, json_record.columns != 'enumValues']
        repeats = pandas.concat([rows] * len(df.index))
        repeats.set_index(df.index, inplace=True)
        flatten_df = pandas.concat([repeats, df], axis=1)
        # append module category / annotating the annotations for module filtering
        flatten_df['module'] = module
        flatten_df.set_index(flatten_df['name'], inplace=True)

        flatten_vals.append(flatten_df)

    flatten_vals.append(empty_vals)

    return flatten_vals


def rightJoin(df1, df2, key, suffixes):
    # rows in df2 that are not in df1 based on unique keys (can be a list) 
    df3 = pandas.merge(df1, df2, on=key, how='right', indicator='Exist', suffixes=suffixes)
    df3['Exist'] = numpy.where(df3.Exist == 'both', True, False)
    return df3


def outerJoin(df1, df2):
    # rows in df1 that are not in df2 
    df3 = pandas.merge(df1, df2, how='outer', indicator=True).query('_merge == "left_only"').drop(['_merge'], axis=1)
    return df3


def updateTable(tableSynId, newTable, key, delta=False, whereClause=False):
    """
    A table may have one-many key(s) in a table schema predefined by the user
    There are three cases where changes can be done to a table:

        Case 1: The unique keys have been changed but the remaining schema is the same
        Case 2: The schema has been changed but the keys are the same
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
        sys.exit("All of the unique keys (key | value) in schema don't exist")
    elif sum(pandas.Series(key).isin(currentTable.columns)) == 1:
        sys.exit("One of the unique keys (key | value) in schema don't exist")
    else:
        logging.info("Unique keys in schema exist and pursuing")

    # Test cases: change a non-key column cell (valuesDescription) and change a unique key cell (value)
    # newTable.iloc[3, newTable.columns.get_loc('valuesDescription')] = 'exome sequencing Nasim'
    # newTable.iloc[1, newTable.columns.get_loc('value')] = 'Nasim'

    # standardize na/NAN in data by replacing it with an empty string for match comparisons
    currentTable = currentTable.fillna("")
    newTable = newTable.fillna("")

    # Match schema in current and new tables
    schema = currentTable.columns
    newTable = newTable[currentTable.columns]

    # Keep the ROW_ID of the current Table
    currentTable['index'] = currentTable.index

    ## Case 1: find the rows where the unique keys have been changed but the remaining schema is the same
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

    ## Case 2: The schema has changed but the keys are the same
    currentUpdated = outerJoin(currentTable, newTable)
    changedSchema = outerJoin(currentUpdated, changedKeysRows)

    ##  Case 1 or 2: Remove changed rows in current table
    if not changedSchema.empty or not changedKeysRows.empty:

        if not changedSchema.empty and changedKeysRows.empty:
            logging.info("Deleting rows with updated schema")
            changedSchema.set_index('index', inplace=True, drop=True)
            toDelete = changedSchema
            deleteRows = syn.delete(Table(syn.get(tableSynId), toDelete))

        if not changedKeysRows.empty and changedSchema.empty:
            logging.info("Deleting rows with updated keys")
            changedKeysRows.set_index('index', inplace=True, drop=True)
            toDelete = changedKeysRows
            deleteRows = syn.delete(Table(syn.get(tableSynId), toDelete))

        if not changedSchema.empty and not changedKeysRows.empty:
            logging.info("Deleting rows with updated keys and schema")
            changedSchema.set_index('index', inplace=True, drop=True)
            changedKeysRows.set_index('index', inplace=True, drop=True)
            toDelete = pandas.concat([changedKeysRows, changedSchema])
            deleteRows = syn.delete(Table(syn.get(tableSynId), toDelete))

        else:
            logging.info("No rows to delete in current table")

    # Case 1,2,3: All new or updated rows to be added to table
    newOrUpdated = outerJoin(newTable, currentTable)
    newOrUpdated = newOrUpdated[schema]
    newOrUpdated.sort_values(['key', 'value'], ascending=[True, True], inplace=True)
    if not newOrUpdated.empty:
        logging.info("Storing new and updated changes")
        table = syn.store(Table(syn.get(tableSynId), newOrUpdated))


def main():
    for i, p in enumerate(paths):
        data = json2flatten(p, names[i])
        module_df = pandas.concat(data)
        all_modules.append(module_df)

    # append/concat/collapse all normalized dataframe annotations into one dataframe
    all_modules_df = pandas.concat(all_modules)

    # re-arrange columns/fields
    all_modules_df = all_modules_df[
        ["name", "description", "columnType", "maximumSize", "enumValues_value", "enumValues_description",
         "enumValues_source", "module"]]

    all_modules_df.columns = ["key", "description", "columnType", "maximumSize", "value", "valuesDescription",
                               "source", "module"]

    # save the table as a csv file
    all_modules_df.sort_values(['key', 'value'], ascending=[True, True], inplace=True)
    all_modules_df.to_csv("annot.csv", sep=',', index=False, encoding="utf-8")
    all_modules_df = pandas.read_csv('annot.csv', delimiter=',', encoding="utf-8")
    os.remove("annot.csv")

    updateTable(tableSynId=tableSynId, newTable=all_modules_df, key=key, delta=False, whereClause=False)


if '__main__' == __name__:
    main()

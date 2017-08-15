import os
import sys
import requests
import json
import pandas
import synapseclient
from nose.tools import assert_equals
from pandas.util.testing import assert_frame_equal

syn = synapseclient.login()

tableSynId = "syn10265158"

all_modules = []
key = ["key", "value", "module"]
annotation_schema = ["key", "description", "columnType", "maximumSize", "value", "valuesDescription",
                     "source", "module"]

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

currentTable = syn.tableQuery("SELECT * FROM %s" % tableSynId)
currentTable = currentTable.asDataFrame()



def check_keys():
    """
    Example: nosetests -vs tests/unit/test_json2synapse.py:check_keys
    :return: None or assert_equals Error message
    """
    for module, path in names.iteritems():
        table_key_set = set(currentTable[currentTable['module'] == module].key.unique())
        json_record = pandas.read_json(path)
        json_key_set = set(json_record['name'])
        # print("json_key_set", len(json_key_set), json_key_set)
        # print("table_key_set", len(table_key_set), table_key_set)
        assert_equals(len(json_key_set), len(table_key_set), ' '.join(["module name:", module, "synapseAnnotations "
                                                                                                 "github repo keys "
                                                                                                 "length",
                                                                       str(len(json_key_set)), "don't match synapse "
                                                                                               "table "
                                                                                               "length",
                                                                       str(len(table_key_set))]))


def compare_key_values():
    """
    Example: nosetests -vs tests/unit/test_json2synapse.py:compare_key_values

    :return: If the synapse table key-value columns data frame matches exactly with the normalized
    json key-value columns data frame it returns None otherwise it generates an error with the % mismatch.

    It is required for both data frames to be sorted exactly the same, otherwise a small % mismatch is reported.
    """
    # subset dataframe to only compare the unique keys (key-value)
    key = ['key', 'value']
    synapse_df = currentTable.loc[:, ('key', 'value')]
    github_df = all_modules_df.loc[:, ('key', 'value')]

    # sort by key (key-value pair)
    synapse_df.sort_values(key, ascending=[True, True], inplace=True)
    github_df.sort_values(key, ascending=[True, True], inplace=True)

    # set the columns as index (may not be needed)
    synapse_df.set_index(key, inplace=True, drop=False)
    github_df.set_index(key, inplace=True, drop=False)

    # reset the index (pandas assigns unique labels per each multi-key value)
    synapse_df.reset_index(inplace=True, level=None, drop=True)
    github_df.reset_index(inplace=True, level=None, drop=True)

    #synapse_df.to_csv("df1.csv")
    #github_df.to_csv("df2.csv")

    # compare the dataframes
    assert_frame_equal(github_df, synapse_df, check_names=False)


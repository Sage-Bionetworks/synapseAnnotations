import pandas
import synapseclient
from pandas.io.json import json_normalize

syn = synapseclient.login()

# TODO: replace with auto download of all github raw files in repositority 
standard_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_standard.json'
analysis_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_analysis.json'
dhart_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/dhart_annotations.json'
genie_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/genie_annotations.json'
neuro_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/neuro_annotations.json'
nf_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/nf_annotations.json'
ngs_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/ngs_annotations.json'
onc_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/onc_annotations.json'

# global variables: paths to raw json files and their project name
paths = [standard_path, analysis_path, dhart_path, genie_path, neuro_path, nf_path, ngs_path, onc_path]
names = ['standard', 'analysis', 'dhart', 'genie', 'neuro', 'nf', 'ngs', 'onc']

# for each project save normalized json to a list
all_projects = []


def json2flatten(path, project):
    # fetch and read raw json objects from its github url and decode the json object to its raw format
    json_record = pandas.read_json(path)

    # for each value list object save normalized df to a list
    flatten_vals = []

    for i, jsn in enumerate(json_record['enumValues']):
        if not json_record['enumValues'][i]:
            # replace NAN / NA with enumvalue objects with an uniform schema holding empty strings
            rows = json_record.ix[i:i, json_record.columns != 'enumValues']
            rows["values_description"] = ""
            rows["source"] = ""
            rows["value"] = ""
            flatten_df = rows
        else:
            df = pandas.io.json.json_normalize(json_record['enumValues'][i])
            # re-name columns to match table on synapse schema (syn9817606)
            df = df.rename(columns={'value': 'enumValues_value', 'description': 'enumValues_description',
                                    'source': 'enumValues_source'})

            # grab key information in its row, expand it by values dimention and append its key-columns to flattened
            # values
            rows = json_record.ix[i:i, json_record.columns != 'enumValues']
            repeats = pandas.concat([rows] * len(df.index))
            repeats.set_index(df.index, inplace=True)
            flatten_df = pandas.concat([repeats, df], axis=1)

            # append project category / annotating the annotations for project filtering
            flatten_df['project'] = project
            flatten_df.set_index(flatten_df['name'], inplace=True)

            flatten_vals.append(flatten_df)

    return flatten_vals


for i, p in enumerate(paths):
    data = json2flatten(p, names[i])
    project_df = pandas.concat(data)
    all_projects.append(project_df)

# append/concat/collapse all normalized dataframe annotations into one dataframe
all_projects_df = pandas.concat(all_projects)

# re-arrange columns/fields 
all_projects_df = all_projects_df[
    ["name", "description", "columnType", "maximumSize", "enumValues_value", "enumValues_description",
     "enumValues_source", "project"]]

# html sources requires to be in utf-8 encode format
all_projects_df.enumValues_description = all_projects_df.enumValues_description.str.encode("utf-8")
all_projects_df.enumValues_source = all_projects_df.enumValues_source.str.encode("utf-8")
all_projects_df.enumValues_value = all_projects_df.enumValues_value.str.encode("utf-8")

# TODO:  update table without appending existing rows in table (Tom | Bruce)
# Temporary solution: save file to a csv file
all_projects_df.to_csv("annot.csv", sep=',', index=False, encoding="utf-8")











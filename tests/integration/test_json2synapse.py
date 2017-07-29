import pandas
import synapseclient
from nose.tools import assert_equals

syn = synapseclient.login()

standard_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_standard.json'
analysis_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_analysis.json'
dhart_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/dhart_annotations.json'
genie_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/genie_annotations.json'
neuro_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/neuro_annotations.json'
nf_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/nf_annotations.json'
ngs_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/ngs_annotations.json'
onc_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/onc_annotations.json'
tool_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/tool_annotations.json'
toolExtended_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/toolExtended_annotations.json'

paths = [standard_path, analysis_path, dhart_path, genie_path, neuro_path, nf_path, ngs_path, onc_path, tool_path, toolExtended_path]
names = ['standard', 'analysis', 'dhart', 'genie', 'neuro', 'nf', 'ngs', 'onc', 'tool', 'toolExtended']

tableSynId = "syn10242922"

currentTable = syn.tableQuery("SELECT * FROM %s" % tableSynId)
currentTable = currentTable.asDataFrame()


def check_keys():
    """
    Example: nosetests -vs tests/integration/test_json2synapse.py:check_keys
    :return: None or Error
    """
    for i, p in enumerate(paths):
        table_key_set = set(currentTable[currentTable['project'] == names[i]].key.unique())
        json_record = pandas.read_json(p)
        json_key_set = set(json_record['name'])
        #print("json_key_set", len(json_key_set), json_key_set)
        #print("table_key_set", len(table_key_set), table_key_set)
        assert_equals(len(json_key_set), len(table_key_set))


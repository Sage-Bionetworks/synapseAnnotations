"""Tests for json files.

"""

import os
import glob
import json


def setup_module(module):
    # Get a list of JSON files
    test_file = os.path.abspath(__file__)
    test_dir = os.path.split(test_file)[0]
    module.json_files = map(lambda x: os.path.abspath(x),
                            glob.glob("%s/../../synapseAnnotations/data/*.json" % test_dir))


def test_duplicate_values_within_key():
    for json_file in json_files:
        with open(json_file) as f:
            d = json.load(f)
            for i in d:
                k = i['name']
                v = [x.get('value') for x in i.get('enumValues') or []]
                value_count = set([x for x in v if v.count(x) > 1])
                if value_count:
                    raise ValueError(
                        "Duplicate values for key '%s': %s in %s" % (k,
                                                                     list(value_count),
                                                                     json_file))

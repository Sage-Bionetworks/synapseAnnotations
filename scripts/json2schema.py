"""Convert an annotations JSON file to a Synapse Table Schema.

This script takes a JSON-formatted annotation definition file (annotation name and allowed values)
converts them it a Synapse Table Schema, and stores it to a Synapse Table.

It is naive in terms of type discovery, using the following hierarchy:

null (string) > boolean > integer > double > string

It can (optionally) take a JSON file of column definitions formatted for Synapse Table schemas.

"""

import json
import urllib
import urlparse
import os
import collections

import synapseclient

def path2url(path):
    """Convert path to URL, even if it already is a URL.

    """

    if path.startswith("/"):
        new_path = urlparse.urljoin('file:', urllib.pathname2url(os.path.abspath(path)))
    else:
        new_path = path

    return new_path

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Convert JSON to Synapse Table Schema')
    parser.add_argument('path', type=str, help='Path (or URL) to JSON file')
    parser.add_argument('--projectId', type=str, help='Synapse Project ID to store schema')
    parser.add_argument('-n', '--dry_run', action="store_true", default=False,
                        help='Dry run')
    parser.add_argument('--synapseJSONSchema', action="store_true",
                        default=False,
                        help="JSON is already in Synapse Table Schema format")
    args = parser.parse_args()

    syn = synapseclient.login(silent=True)

    project = syn.get(args.projectId)

    f = urllib.urlopen(path2url(args.path))
    data = json.load(f)

    url_path = urllib.splittype(args.path)[1]
    filename = os.path.split(url_path)[1]
    schema_name = os.path.splitext(filename)[0]

    if args.synapseJSONSchema:
        schema = synapseclient.Schema(name=schema_name, parent=project)
        schema.columns_to_store = data
    else:
        cols = []

        for k, v in data.iteritems():

            # Handle null values, assume that they will be strings
            if not v:
                column_type = "STRING"
            elif bool in map(type, v):
                column_type = "BOOLEAN"
            elif int in map(type, v):
                column_type = "INTEGER"
            elif float in map(type, v):
                column_type = "DOUBLE"
            else:
                column_type = "STRING"

            cols.append(synapseclient.Column(name=k, columnType=column_type,
                                             enumValues=v, maximumSize=250))

        schema = synapseclient.Schema(name=schema_name, columns=cols, parent=project)

    if args.dry_run:

        schema_as_list = map(dict, schema.columns_to_store)
        new_schema_as_list = []

        _key_order = ['name', 'description', 'columnType', 'maximumSize', 'enumValues', 'defaultValue']

        for col in schema_as_list:
            col['description'] = ""
            col['source'] = ""
            col['defaultValue'] = ""
            
            new_enum_values = []

            for v in col['enumValues']:

                new_value_ordered_dict = collections.OrderedDict()

                new_value_ordered_dict['value'] = v
                new_value_ordered_dict['description'] = ""
                new_value_ordered_dict['source'] = ""

                new_enum_values.append(new_value_ordered_dict)

            col['enumValues'] = new_enum_values

            new_ordered_dict = collections.OrderedDict()
            for k in _key_order:
                new_ordered_dict[k] = col[k]

            new_schema_as_list.append(new_ordered_dict)

        print json.dumps(new_schema_as_list, indent=2)
    else:
        schema = syn.store(schema)

if __name__ == "__main__":
    main()

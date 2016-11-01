'''
This script takes a set of annotation dictionaries and formats them in a more
human-readable format.

'''

from argparse import ArgumentParser
import os
import yaml,json

def formatFromFile(dictionaryList,outputFile='termList.csv'):
    '''
    Formats YAML/JSON to a file with two columns, one for key and one for
    possible values. Can be augmented to provide other formats
    '''
    outfile=open(outputFile,'w')
    outfile.write('Key,Value\n')
    dicts=dictionaryList.split(',')
    for di in dicts:
        base,ext=os.path.splitext(os.path.basename(di))
        f=open(di,'r')
        if ext=='.json':
            data=json.load(f)
        elif ext=='.yml':
            data=yaml.load(f)
        else:
            print 'File %s cannot be parsed because it should be in YAML or JSON \
    format'%(di)
        print 'Loaded dictionary with %d keys'%(len(data))
        for k in data.keys():
            #print data[k]
            if data[k] is None:
                outfile.write('%s,%s\n'%(k,''))
            else:
                for v in data[k]:
                    outfile.write('%s,%s\n'%(k,v))
    outfile.close()



def formatFromSchema(schemaList):
    schemas=schemaList.split(',')
    #TODO: implement this once I figure out schemas


def main():
    #PARSING PARAMETERS
    parser = ArgumentParser(description='Creates human-readable list of possible \
    key-value pairs')
    parser.add_argument('--dictionaries',
                        help='Comma-delimited \
                        paths to YAML/JSON formatted dictionaries',default='')
    parser.add_argument('--tableSchemas',help='Comma-delimited \
    list of synapse IDs to be used as dictionaries',default='')

    args=parser.parse_args()

    if args.dictionaries=='' and args.tableSchemas=='':
        print 'You must provide at least a file or synapseID'

    if args.dictionaries!='':
        formatFromFile(args.dictionaries)
    elif args.tableSchemas!='':
        formatFromSchema(args.tableSchemas)

if __name__=='__main__':
    main()

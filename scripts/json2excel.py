import json
import pandas as pd
import os
import urlparse
import urllib

def conver2excel(dicts, outputFile):
    key_des = pd.DataFrame()
    value_des = pd.DataFrame()
    for di in dicts:
        if urlparse.urlparse(di).scheme != '':
            jfile = urllib.urlopen(di)
        else:
            jfile = open(di,'r')
        base,ext=os.path.splitext(os.path.basename(di))
        if ext=='.json':
            data=json.load(jfile)
        else:
            print 'File %s cannot be parsed because it should be in JSON.' % di
        data = pd.DataFrame(data)
        temp = data.loc[:,['name','description','columnType']]
        temp['category'] = base
        key_des = pd.concat([temp,key_des])
        k_v_data = data.loc[:,['name','enumValues']]
        for index, row in k_v_data.iterrows():
            temp= pd.DataFrame(row['enumValues'])
            temp['key'] = row['name']
            value_des = pd.concat([value_des,temp])
    
    # Change column names and order
    key_des.rename(columns={'name':'key'}, inplace=True)
    value_des = value_des.loc[:,['key','value','description','source']]
    template = pd.DataFrame(columns=pd.concat([pd.Series(['synapseId','fileName']),key_des.key]))

    writer = pd.ExcelWriter(outputFile)
    template.to_excel(writer,'template',index=False)
    key_des.to_excel(writer,'key description',index=False)
    value_des.to_excel(writer,'key-value description',index=False)
    writer.save()
    print("Done.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Create an annotation template excel file with key and value descriptions')

    parser.add_argument('-f','--files',
                        help='Path(s) to JSON file(s)', nargs='+',required = True)
    parser.add_argument('--output',help='output file name',default='output.xlsx',type=str)

    args=parser.parse_args()

    conver2excel(args.files,args.output)

if __name__=='__main__':
    main()
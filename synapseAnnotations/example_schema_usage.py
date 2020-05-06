import json
import os
import pprint

from MetadataModel import MetadataModel
from ManifestGenerator import ManifestGenerator

from config import credentials, schema

pp = pprint.PrettyPrinter(indent = 3)

inputMModelLocation = schema["schemaLocation"]
inputMModelLocationType = "local"

component = "Patient"

mm = MetadataModel(inputMModelLocation, inputMModelLocationType)


print("*****************************************************")
print("Testing metamodel-based manifest generation")
print("*****************************************************")

# testing manifest generation; manifest is generated based on a jsonSchema parsed from Schema.org schema; this generates a google sheet spreadsheet; 

# to generate the sheet, the backend requires Google API credentials in a file credentials.json stored locally in the same directory as this file

# this credentials file is also stored on Synapse and can be retrieved given sufficient permissions to the Synapse project

# Google API credentials file stored on Synapse 
credentials_syn_file = credentials["googleSynId"]

# try downloading credentials file, if needed 
if not os.path.exists("./credentials.json"):
    
    print("Retrieving Google API credentials from Synapse")
    import synapseclient

    syn = synapseclient.Synapse()
    syn.login()
    syn.get(credentials_syn_file, downloadLocation = "./")
    print("Stored Google API credentials")

print("Google API credentials successfully located")


print("Testing manifest generation based on a provided Schema.org schema")
#manifestURL = mm.getModelManifest("Test_" + component, component, filenames = ["1.txt"])
manifestURL = mm.getModelManifest("Test_" + component, component)

print(manifestURL)

print("*****************************************************")
print("Testing metamodel-based validation")
print("*****************************************************")
manifestPath = "./example_manifest.csv"

print("Testing validation with jsonSchema generation from Schema.org schema")
annotationErrors = mm.validateModelManifest(manifestPath, component)
pp.pprint(annotationErrors)

print("*****************************************************")
print("Testing metamodel-based manifest population")
print("*****************************************************")

manifestPath = "./example_manifest.csv"
print("Get a sheet prepopulated with an existing manifest; this is an example manifest")
prepopulatedManifestURL = mm.populateModelManifest("Test_" + component, manifestPath, component)
print(prepopulatedManifestURL)

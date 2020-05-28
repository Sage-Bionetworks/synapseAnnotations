"""
Stores config variables to be used in other modules
"""

# asset storage parameters
storage = {
    "Synapse":{
      #synapse ID of fileview containing administrative storage metadata; 
      "masterFileview":"syn20446927",
      # default manifest name 
      "manifestFilename":"synapse_storage_manifest.csv"
    }
}


# credentials parameters
credentials = {
        # Synapse ID of entity storing 
        # google account OAuth credentials file
        "googleSynId":"syn21088684",
        # path to cached credentials file
        "path":"./credentials.json"
}


# data model and schema related parameters
schema = {
    "schemaLocation": "./schemas/example.jsonld"
}


# app and manifest style (colors, alignments, etc.)
style = {
        "googleManifest":{
            #required columns/cells background color
            "reqBgColor":{
                        'red': 235.0/255,
                        'green': 248.0/255,
                        'blue': 250.0/255
            },
            #optional columns/cells background color
            "optBgColor":{
                        'red': 255.0/255,
                        'green': 255.0/255,
                        'blue': 230.0/255
            }
        }
}

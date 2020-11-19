######################################
####  Bind test schema to entity  ####
######################################

## Testing out binding the schema that references synapseAnnotations terms, and
## validating annotations against it.

library("glue")
synLogin()

## Bind testschema.json to entity
synRestPUT(
  uri = "/entity/syn23555343/schema/binding",
  body = '{entityId: "syn23555343", schema$id: "karatestorg20201105-testschema.json-0.0.2"}'
)

synRestGET(uri = "/entity/syn23555343/schema/binding")

## Add some files to the project
write("testing a file with valid annotations", "valid.txt")
write("testing a file with invalid annotations", "invalid.txt")

## Valid annotations
valid <- File(
  path = "valid.txt",
  parent = "syn23555343",
  annotations = list(
    resourceType = "experimentalData",
    consortium = "AMP-AD",
    study = "iPSCAstrocytes",
    fileFormat = "bam",
    assay = "rnaSeq",
    species = "Mouse"
    )
)

## Invalid annotations
invalid <- File(
  path = "invalid.txt",
  parent = "syn23555343",
  annotations = list(
    resourceType = "experimentalData",
    consortium = "AMP-AD",
    study = "iPSCAstrocytes",
    assay = "ChIPSeq",
    species = "Mouse"
  )
)

synStore(valid)
synStore(invalid)

## Clean up local files
file.remove(c("valid.txt", "invalid.txt"))

synRestGET("/entity/syn23555348/schema/validation")
synRestGET("/entity/syn23555349/schema/validation")

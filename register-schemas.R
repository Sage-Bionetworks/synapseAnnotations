############################################
####  Register mini-schemas in Synapse  ####
############################################

library("synapser")
library("fs")
library("here")
library("purrr")
library("glue")

synLogin()

# Function to register JSON schema file ----------------------------------------

create_body <- function(file) {
  paste(
    '{"concreteType": "org.sagebionetworks.repo.model.schema.CreateSchemaRequest", "schema": ',
    paste(readLines(file), collapse = ""),
    '}'
  )
}

register_schema <- function(file) {
  synRestPOST(
    uri = "/schema/type/create/async/start",
    body = create_body(file)
  )
}

# Register terms ---------------------------------------------------------------

term_files <- dir_ls(here("terms"), regexp = "*\\.json", recurse = 1)

## Register each mini-schema
walk(term_files, register_schema)

## List all schemas to check they're there
synRestPOST(
  uri = "/schema/list",
  body = '{organizationName: "sage.annotations"}'
)

# Register top-level schema ----------------------------------------------------

token <- register_schema(here("schemas", "testschema.json"))

# Retrieve schema
synRestGET(uri = glue("/schema/type/create/async/get/{token$token}"))

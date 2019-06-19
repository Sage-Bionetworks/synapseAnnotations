######################################################################
####  Convert annotations controlled vocabularies to JSON schema  ####
######################################################################

## This script converts our annotations definitions to JSON schema format. These
## definitions, and the schemas built upon them, are intended to serve as a
## groundtruth for automatically generated schemas, however the schemas
## generated from schema.org JSON-LD files will be simpler in at least one
## important way: currently, to retain information about the source and
## description of each term, this script defines enumerated values as separate
## `"const"` items rather than an enumerated list. This will not be necessary if
## this information is captured in the schema.org source.

library("purrr")
library("rlang")
library("jsonlite")
library("here")
library("tools")
library("fs")

## Convert our enumerated values objects with description etc. into schema
## objects (with value as "const" and additional properties for description and
## source)
create_enum <- function(list) {
  list(const = list$value, description = list$description, source = list$source)
}

## Given an annotation entry, convert it to JSON Schema format
create_schema_from_entry <- function(x) {
  desc <- x$description %||% ""
  if (length(x$enumValues) > 0) {
    ## If there are enum values, turn those into objects using `"const"` so we
    ## can attach description and source as well
    enum <- purrr::map(x$enumValues, create_enum)
    ret <- list(
      name = list(
        description = desc,
        anyOf = enum
      )
    )
  } else if (!is.null(x$columnType)) {
    ## Some annotations just have a column type; in that case set this to "type"
    ret <- list(
      name = list(
        description = desc,
        type = switch(
          x$columnType,
          "STRING" = "string",
          "BOOLEAN" = "boolean",
          "INTEGER" = "integer",
          "DOUBLE" = "number"
        )
      )
    )
  }
  names(ret) <- x$name
  ret
}

## Given a set of entries (e.g. one file from our synapseAnnotations/data/
## folder), create a set of definitions
create_schema_from_entries <- function(x) {
  if (is.atomic(x[[1]])) {
    x <- list(x)
  }
  map(x, create_schema_from_entry) %>%
    unlist(recursive = FALSE)
}

## Add additional JSON Schema stuff and convert to JSON
create_output_json <- function(definitions, name) {
  list(
    "$schema" = "http://json-schema.org/draft-07/schema#",
    "$id" = paste0("http://example.com/", name),
    "definitions" = definitions
  ) %>%
    toJSON(auto_unbox = TRUE, pretty = TRUE)
}

## List json files
files <- list.files(
  here("synapseAnnotations/data/original"),
  full.names = TRUE
)
names(files) <- basename(files)

## Create the JSON schema data
json_data <- files %>%
  map(read_json, simplifyVector = FALSE) %>%
  map(create_schema_from_entries) %>%
  imap(create_output_json)

dir_create(here("synapseAnnotations/data/json-schemas-from-original/definitions"))

## Output JSON schema definitions
iwalk(
  json_data,
  function(x, y) {
    write(x, here("synapseAnnotations/data/json-schemas-from-original/definitions", y))
  }
)

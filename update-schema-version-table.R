#!/usr/local/bin/Rscript
###############################################################
####  Update the Synapse Annotations Schema Version table  ####
###############################################################

library("jsonlite")
library("tidyverse")
library("synapser")
library("glue")
library("here")

## Helper functions ------------------------------------------------------------

#' Extract module or annotation key name from $id field
#'
#' @param id string containing the schema `$id`
#' @param info one of "id" (organization-module.key), "module", "key",
#' or "version"
#' @param absolute_path string containing the absolute path prefix to remove
#' @return The id, module, key, or version
get_info <- function(id, info = c("id", "module", "key", "version"),
                     absolute_path = "https://repo-prod.prod.sagebase.org/repo/v1/schema/type/registered/") {
  ## Remove absolute path for simpler regex; we know the format for Sage schemas
  id <- gsub(absolute_path, "", id)
  info <- match.arg(info)
  pattern <- "^[^-]+-([[:alnum:]]+)\\.([[:alnum:]]+)-([0-9\\.]+)"
  switch(
    info,
    id = gsub("-[0-9\\.]+$", "", id),
    module = gsub(pattern, "\\1", id),
    key = gsub(pattern, "\\2", id),
    version = gsub(pattern, "\\3", id)
  )
}

#' Extract file path from referenced id
#'
#' @param id string containing the schema `$id`
#' @return The local file path to the schema for the `$id`
get_ref_path <- function(id) {
  module <- get_info(id, "module")
  key <- get_info(id, "key")
  glue::glue("{here('terms')}/{module}/{key}.json")
}

#' Create table row for tracking schema versions
#'
#' @param file Path to the JSON Schema file.
#' @return
create_rows_schema <- function(file) {
  dat <- fromJSON(file)
  ## Grab information from the full id
  tibble::tibble(
    key = get_info(dat$`$id`, "key"),
    latestVersion = get_info(dat$`$id`, "version"),
    schema = get_info(dat$`$id`, "id"),
    module = get_info(dat$`$id`, "module")
  )
}

## -----------------------------------------------------------------------------

## Log in to synapse
synLogin()

## JSON files
files <- list.files(
  here("terms"),
  # here("terms"),
  pattern = "\\.json$",
  full.names = TRUE,
  recursive = TRUE
)

## Update schema version table
dat_schema <- map_dfr(files, create_rows_schema)

## Delete old table rows
schema_table <- "syn26050066"
current_schema <- synTableQuery(glue("SELECT * FROM {schema_table}"))
synDelete(current_schema) # delete current rows

## Update table rows
temp_schema <- tempfile()
write_csv(dat_schema, temp_schema, na = "")
new_schema <- Table(schema_table, temp_schema)
synStore(new_schema)

## Query to force table index to rebuild
synTableQuery(glue("SELECT ROW_ID FROM {schema_table}"))

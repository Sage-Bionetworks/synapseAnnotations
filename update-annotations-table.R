#!/usr/local/bin/Rscript
################################################
####  Update the Synapse Annotations table  ####
################################################

library("jsonlite")
library("tidyverse")
library("synapser")
library("glue")
library("httr")
library("here")

"%||%" <- function(a, b) {
  if (!is.null(a)) a else b
}

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

#' Append enumerated values for a term
#'
#' @param data_table Table with columns key, description, columnType, module,
#' maximumSize for adding the enumerated values of the key to
#' @param json_list List of json data from the file
#' @return Table with columns key, description, columnType, module, maximumSize,
#' value, valueDescription, source, with one row per enumerated value
add_enumerated_values <- function(data_table, json_list) {
  enum_df <- json_list[["anyOf"]] %>%
    rename(
      value = const,
      valueDescription = description
    ) %>%
      mutate(value = as.character(value))
  return_df <- full_join(data_table, enum_df, by = character())
  ## If no value had a source, then need to add this column
  if (!("source" %in% names(return_df))) {
    return_df <- return_df %>%
      add_column(source = NA)
  }
  return(return_df)
}

#' Create table row(s) for a term
#'
#' @param file Path to the JSON Schema file containing a term. For terms that
#' reference enumerated values of a different term, the referenced term
#' should exist as a file in the current set. The referenced term cannot be
#' extended.
#' @return
create_rows_dict <- function(file) {
  dat <- fromJSON(file)
  ## Information about the key
  return_df <- tibble::tibble(
    key = get_info(dat$`$id`, "key"),
    description = dat$description %||% NA_character_,
    columnType = dat$type %||% "string",
    module = get_info(dat$`$id`, "module"),
    maximumSize = NA_real_
  )
  ## If term has enumerated values in anyOf, fromJSON will create a handy data
  ## frame of those. We use that in combination with return_df to create a row
  ## for each value.
  ## If term references the enumerated values of another term, grab those. Term
  ## cannot extend the values in a referenced schema. Schema referenced should
  ## exist in current set of schema files.
  if ("anyOf" %in% names(dat)) {
    return_df <- add_enumerated_values(data_table = return_df, json_list = dat)
  } else if ("properties" %in% names(dat)) {
    # Assume will be a reference to existing file with enumerated values
    alias_dat <- fromJSON(get_ref_path(dat$properties[[return_df$key]]$`$ref`))
    return_df <- add_enumerated_values(
      data_table = return_df,
      json_list = alias_dat
    )
  } else {
    return_df <- return_df %>%
    add_column(value = NA, valueDescription = NA, source = NA)
  }

  ## Select columns in order that matches the table schema
  select(
    return_df,
    key,
    description,
    columnType,
    maximumSize,
    value,
    valueDescription,
    source,
    module
  )
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
    schema = get_info(dat$`$id`, "id")
  )
}

## Log in to synapse
synLogin()

## JSON files
files <- list.files(
  here("terms"),
  pattern = "\\.json$",
  full.names = TRUE,
  recursive = TRUE
)

## Dictionary table
dat_dict <- map_dfr(files, create_rows_dict)

## Delete old table rows
annots_table <- "syn10242922"
current <- synTableQuery(glue("SELECT * FROM {annots_table}"))
synDelete(current) # delete current rows

## Update table rows
temp <- tempfile()
write_csv(dat_dict, temp, na = "")
new <- Table(annots_table, temp)
synStore(new)

## Query to force table index to rebuild
synTableQuery(glue("SELECT ROW_ID FROM {annots_table}"))

################################################
####  Update the Synapse Annotations table  ####
################################################

library("jsonlite")
library("tidyverse")
library("reticulate")
library("glue")
library("httr")
library("here")

## Log in to synapse
synapse <- import("synapseclient")
syn <- synapse$Synapse()
syn$login()

## Get release version
release <- GET("https://api.github.com/repos/Sage-Bionetworks/synapseAnnotations/releases")
body <- content(release)
release_version <- body[[1]]$tag_name

## JSON files
files <- list.files(
  here("synapseAnnotations", "data"),
  full.names = TRUE
)
files <- files[grepl("\\.json$", files)] # no directories
names(files) <- tools::file_path_sans_ext(basename(files))

## Ensure `value` column gets converted to character, otherwise `unnest()`
## complains about incompatible types
value_to_chr <- function(x) {
  if(is.null(x$value)) {
    return(NULL)
  }
  mutate(x, value = as.character(value))
}

## Unnest the enumerated values for each key
unnest_module <- function(x) {
  x %>%
    unnest(
      cols = "enumValues",
      names_repair = "universal",
      keep_empty = TRUE
    ) %>%
    rename(
      ## Rename columns. This works with our current JSON data, but the
      ## numbering of columns could change if we change the underlying data
      ## structure, so pay attention here.
      description = `description...2`,
      valueDescription = `description...6`,
      source = `source...7`
    ) %>%
    ## Drop source column for keys because a) it's not in the synapse table
    ## schema and b) very few keys have a source
    select(-`source...10`)
}

## Load in json data
definitions <- files %>%
  imap_dfr(~ mutate(fromJSON(.x), module = .y)) %>%
  mutate(enumValues = map(enumValues, ~ value_to_chr(.x))) %>%
  unnest_module() %>%
  mutate(source = coalesce(source, Source)) %>%
  select(-Source) %>%
  rename(key = name)

## Delete old table rows
annots_table <- "syn10242922"
current <- syn$tableQuery(glue("SELECT * FROM {annots_table}"))
syn$delete(current) # delete current rows

## Update annotations on the table
table_obj <- syn$get(annots_table)
syn$setAnnotations(table_obj, py_dict("annotationReleaseVersion", release_version))

## Update table rows
temp <- tempfile()
write_csv(definitions, temp, na = "")
new <- synapse$Table(annots_table, temp)
syn$store(new)

## Query to force table index to rebuild
syn$tableQuery(glue("SELECT ROW_ID FROM {annots_table} LIMIT 1"))

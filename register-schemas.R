#!/usr/local/bin/Rscript
doc <- "Register Schemas on Synapse

Usage:
  register-schemas.R <files>... [--dryRun]
  register-schemas.R (-h | --help)
  register-schemas.R --version

Options:
  -h --help    Show this screen.
  --version    Show version.
  --dryRun     Tests if the schema(s) can be registered, but does not actually
               register them.
"

suppressPackageStartupMessages(library("docopt"))
suppressPackageStartupMessages(library("synapser"))
suppressPackageStartupMessages(library("purrr"))
suppressPackageStartupMessages(library("glue"))

opts <- docopt(doc, version = 'Register Schemas 0.1\n')

synLogin()

# Functions to register JSON schema file ---------------------------------------

#' Create schema request body
#'
#' @param file Path to JSON Schema file
#' @param dryRun Should the dryRun field be set to `true`? Defaults to `FALSE`.
#' @return String containing the JSON request body
create_body <- function(file, dryRun = FALSE) {
  stopifnot(dryRun %in% c(TRUE, FALSE))
  paste(
    '{"concreteType": "org.sagebionetworks.repo.model.schema.CreateSchemaRequest", "schema": ',
    paste(readLines(file), collapse = ""),
    ', "dryRun": ',
    ifelse(dryRun, 'true', 'false'),
    '}'
  )
}

#' Register schema to Synapse
#'
#' Given a path to a file containing a JSON schema, registers that schema on
#' Synapse.
#'
#' @param file Path to JSON Schema file
#' @param dryRun Should the dryRun field be set to `true`? Defaults to `FALSE`.
#' @return Token object containing the async token used to monitor the job
register_schema <- function(file, dryRun = FALSE) {
  synRestPOST(
    uri = "/schema/type/create/async/start",
    body = create_body(file, dryRun = dryRun)
  )
}

#' Get status of registered schema
#'
#' @param token Async token
#' @return Response object containing schema
get_registration_status <- function(token) {
  processing <- TRUE
  ## Check results of registering schema, retrying if the async job hasn't
  ## completed yet
  while (processing) {
    result <- synRestGET(
      uri = glue("/schema/type/create/async/get/{token}")
    )
    ## synapser doesn't return the status codes unfortunately, so we check the
    ## response object to determine what to do. If it contains "jobState",
    ## that's part of the AsynchronousJobStatus, i.e. the async job hasn't
    ## completed yet.
    if (!"jobState" %in% names(result)) {
      processing <- FALSE
    }
  }
  result
}

#' Register schema and report on its status
#'
#' Registers a schema and then monitors the asynchronous job until it completes.
#'
#' @param file Path to JSON Schema file
#' @param dryRun Should the dryRun field be set to `true`? Defaults to `FALSE`.
#' @return `TRUE` if schema was successfully registered; `FALSE` otherwise.
register_and_report <- function(file, dryRun = FALSE) {
  message(glue("Registering {file} with dryRun = {dryRun}"))
  ## register_schema() can fail if e.g. schemas contain non-ASCII characters --
  ## in this case we catch that error and provide the message.
  token <- try(register_schema(file, dryRun = dryRun), silent = TRUE)
  if (inherits(token, "try-error")) {
    message(token)
    return(FALSE)
  }
  ## If we get a 400 status code, synapser will throw an error -- we want to
  ## catch that and provide the message but not raise an actual R error.
  status <- try(get_registration_status(token$token), silent = TRUE)
  if (inherits(status, "try-error")) {
    message(status)
    FALSE
  } else {
    TRUE
  }
}

# Register terms ---------------------------------------------------------------

## Register each mini-schema
results <- map_lgl(opts$files, register_and_report, dryRun = opts$dryRun)

if (!all(results)) {
  quit(status = 1)
} else {
  quit(status = 0)
}

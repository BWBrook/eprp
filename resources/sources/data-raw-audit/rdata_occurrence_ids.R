# Distinct PBDB occurrence numbers held in R binaries (.RData, .rda, .rds).
#
# Usage: Rscript rdata_occurrence_ids.R OUT_DIR PREFIX FILE [FILE ...]
#
# embedded_pbdb_check.py (register-deposits) lists R binaries but does not
# read them. This walks every data frame and list in each file and takes any
# column whose name ends in occurrence_no or occurrence.no (optionally with a
# .x suffix), or an oid column of occ: identifiers. Each file with such a
# column gets OUT_DIR/PREFIX__rNNN.ids (one number per line, NNN its position
# in the arguments), the form ids_pbdb_check.py groups by PREFIX. Every data
# frame found is appended as a row to OUT_DIR/rdata_objects.tsv. A file that
# load() rejects is tried with readRDS(), and the reverse for .rds (some
# deposits name a saveRDS file .rda); one that fails both gets a row saying
# so. Base R only.

args <- commandArgs(trailingOnly = TRUE)
out_dir <- args[1]
prefix <- args[2]
files <- args[-(1:2)]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
pat <- "(^|\\.)occurrence[._]no(\\.x)?$"
tab_path <- file.path(out_dir, "rdata_objects.tsv")
if (!file.exists(tab_path)) {
  writeLines(paste("prefix", "file", "object", "nrow", "ncol", "occurrence_column", "distinct_in_file", "ids_file", sep = "\t"), tab_path)
}

walk <- function(x, path, env, depth = 0) {
  if (depth > 40) {
    env$deep <- env$deep + 1
    return(invisible())
  }
  if (is.data.frame(x)) {
    cols <- grep(pat, names(x), ignore.case = TRUE, value = TRUE)
    if (!length(cols) && "oid" %in% tolower(names(x))) {
      v <- as.character(x[[which(tolower(names(x)) == "oid")[1]]])
      if (any(grepl("^occ:[0-9]+$", v))) {
        env$ids <- c(env$ids, as.integer(sub("^occ:", "", v[grepl("^occ:[0-9]+$", v)])))
        cols <- "oid"
      }
    }
    for (cl in setdiff(cols, "oid")) env$ids <- c(env$ids, suppressWarnings(as.integer(as.character(x[[cl]]))))
    env$rows[[length(env$rows) + 1]] <- c(path, nrow(x), ncol(x), if (length(cols)) paste(cols, collapse = ";") else "-")
  } else if (is.list(x) && !isS4(x)) {
    nm <- names(x)
    for (i in seq_along(x)) walk(x[[i]], paste0(path, "$", if (!is.null(nm) && nzchar(nm[i])) nm[i] else i), env, depth + 1)
  }
}

for (k in seq_along(files)) {
  f <- files[k]
  acc <- new.env()
  acc$ids <- integer()
  acc$rows <- list()
  e <- new.env()
  as_rds <- function() assign(sub("\\.(rds|rda|rdata)$", "", basename(f), ignore.case = TRUE), readRDS(f), envir = e)
  first <- if (grepl("\\.rds$", f, ignore.case = TRUE)) as_rds else function() load(f, envir = e)
  second <- if (grepl("\\.rds$", f, ignore.case = TRUE)) function() load(f, envir = e) else as_rds
  ok <- tryCatch({ first(); TRUE }, error = function(err) {
    tryCatch({ second(); TRUE }, error = function(err2) conditionMessage(err))
  })
  if (!isTRUE(ok)) {
    cat(paste(prefix, f, "-", NA, NA, paste("load failed:", gsub("[\t\n]", " ", ok)), 0, "-", sep = "\t"), "\n", sep = "", file = tab_path, append = TRUE)
    next
  }
  acc$deep <- 0
  failed <- character()
  for (o in ls(e, all.names = TRUE)) {
    r <- tryCatch({ walk(get(o, envir = e), o, acc); NULL }, error = function(err) conditionMessage(err))
    if (!is.null(r)) failed <- c(failed, paste0(o, ": ", gsub("[\t\n]", " ", r)))
  }
  if (length(failed)) acc$rows[[length(acc$rows) + 1]] <- c("-", NA, NA, paste("not walked:", paste(failed, collapse = "; ")))
  if (acc$deep) acc$rows[[length(acc$rows) + 1]] <- c("-", NA, NA, paste("lists nested deeper than 40 levels, not walked:", acc$deep))
  ids <- sort(unique(acc$ids[!is.na(acc$ids)]))
  ids_file <- "-"
  if (length(ids)) {
    ids_file <- sprintf("%s__r%03d.ids", prefix, k)
    writeLines(as.character(ids), file.path(out_dir, ids_file))
  }
  if (!length(acc$rows)) acc$rows <- list(c("-", NA, NA, "no data frames"))
  for (r in acc$rows) {
    cat(paste(c(prefix, f, r, length(ids), ids_file), collapse = "\t"), "\n", sep = "", file = tab_path, append = TRUE)
  }
  cat(prefix, " ", basename(f), ": ", length(ids), " distinct occurrence numbers\n", sep = "")
  rm(e)
  invisible(gc())
}

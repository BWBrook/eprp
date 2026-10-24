# Write Aze et al. (2011) Appendix S5 tables, as carried by the CRAN package paleotree, to CSV.
# Usage: Rscript aze_paleotree_tables.R PALEOTREE_TARBALL OUT_DIR
# Base R only: the data file is unpacked from the source tarball and loaded, not the package.
args <- commandArgs(trailingOnly = TRUE)
dir.create(args[2], recursive = TRUE, showWarnings = FALSE)
td <- tempfile()
listing <- untar(args[1], list = TRUE)
data_file <- grep("^paleotree/data/macroperforateForam\\.", listing, value = TRUE)
stopifnot(length(data_file) == 1)
untar(args[1], files = data_file, exdir = td)
e <- new.env()
load(file.path(td, data_file), envir = e)
for (n in ls(e)) {
  x <- e[[n]]
  write.csv(x, file.path(args[2], paste0(n, ".csv")), row.names = !is.null(rownames(x)) && !identical(rownames(x), as.character(seq_len(nrow(x)))))
  cat(n, nrow(x), "rows x", ncol(x), "columns:", paste(head(colnames(x), 8), collapse = ", "), "\n")
}

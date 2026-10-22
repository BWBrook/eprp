# Export the presence table of a Triton RData file as gzipped TSV, unchanged.
# Usage: Rscript triton_export.R TRITON_RDATA OUT_TSV_GZ
# Writes every row and column of the *.pres data frame; filtering (e.g. trim ==
# "inc") is left to the analysis. Prints the row count for checking. Base R only.

args <- commandArgs(trailingOnly = TRUE)
e <- new.env()
load(args[1], envir = e)
pres_name <- grep("\\.pres$", ls(e), value = TRUE)
stopifnot(length(pres_name) == 1)
pres <- get(pres_name, envir = e)
con <- gzfile(args[2], "w")
write.table(pres, con, sep = "\t", quote = FALSE, row.names = FALSE, na = "")
close(con)
cat(pres_name, nrow(pres), "rows,", ncol(pres), "columns\n")

# Tranche-4 geometric Weibull arm (amendment A5 in ../VALIDATION_T4.md): Alroy's richness package per bin,
# on occurrence frequencies and on individual counts.
# Usage: Rscript t4_gw.R <data dir> <tag> <out csv> <ML or ML,LD>
suppressPackageStartupMessages(library(richness))
args <- commandArgs(TRUE)
occ <- read.csv(file.path(args[1], paste0("occ_", args[2], ".csv.gz")))
methods <- strsplit(args[4], ",")[[1]]
fits <- list(ML = cegsML, LD = cegsLD)
fit <- function(f, n) tryCatch(suppressWarnings(f(n)$richness), error = function(e) NA_real_)

one <- function(x) {
  inc <- as.vector(table(x$species))
  abund <- as.vector(tapply(x$n, x$species, sum))
  out <- data.frame(rep = x$rep[1], bin = x$bin[1], S = length(inc))
  for (m in methods) {
    out[[paste0("gw_", tolower(m), "_inc")]] <- fit(fits[[m]], inc)
    out[[paste0("gw_", tolower(m), "_abund")]] <- fit(fits[[m]], abund)
  }
  out
}
res <- parallel::mclapply(split(occ, list(occ$rep, occ$bin), drop = TRUE), one, mc.cores = as.integer(Sys.getenv("BENCH_CORES", "12")))
bad <- !sapply(res, is.data.frame)
if (any(bad)) stop("cells failed: ", paste(names(res)[bad], collapse = ", "))
res <- do.call(rbind, res)
write.csv(res[order(res$rep, res$bin), ], args[3], row.names = FALSE)

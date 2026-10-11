# Inspect two pinned source objects; do not run the source analysis or fit models.
# Usage: Rscript --vanilla data/q050-covariance-support/inspect.R ZIP [OUTPUT]
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1L || length(args) > 2L) stop("Supply ZIP and optional output TSV")
archive <- args[1L]
output <- if (length(args) == 2L) args[2L] else "data/q050-covariance-support/summary.tsv"
stopifnot(unname(tools::md5sum(archive)) == "ab026931157f5734790be0ed732dc94b")

prefix <- "NiklasHohmann-paradox_of_predictability-9a47ba6/data/"
members <- paste0(prefix, c(
  "Brombacher.et.al_2017_Globoconella_puncticulata.Rdata",
  "Brombacher.et.al_2017_Truncorotalia_crassaformis.Rdata"
))
listing <- unzip(archive, list = TRUE)
stopifnot(all(members %in% listing$Name))
expected_fields <- c("nsamp", "nvar", "M", "S", "nn", "tt",
                     "time.units", "taxon", "sex", "reference")

objects <- lapply(members, function(member) {
  con <- unz(archive, member, open = "rb")
  on.exit(close(con))
  e <- new.env(parent = emptyenv())
  loaded <- load(con, envir = e)
  stopifnot(length(loaded) == 1L)
  x <- e[[loaded]]
  stopifnot(setequal(names(x), expected_fields), x$nvar == 2L,
            identical(dim(x$M), c(x$nsamp, 2L)),
            length(x$S) == x$nsamp, length(x$nn) == x$nsamp,
            length(x$tt) == x$nsamp,
            all(is.finite(x$M)), all(is.finite(unlist(x$S))),
            all(is.finite(x$nn)), all(x$nn >= 2), all(x$nn == as.integer(x$nn)),
            all(is.finite(x$tt)), x$tt[1L] == 0, all(diff(x$tt) > 0),
            x$time.units == "Myr")
  for (s in x$S) {
    stopifnot(identical(dim(s), c(2L, 2L)),
              max(abs(s - t(s))) < 1e-12,
              min(eigen(s, symmetric = TRUE, only.values = TRUE)$values) > 0,
              identical(rownames(s), c("Area", "Aspect_ratio")),
              identical(colnames(s), c("Area", "Aspect_ratio")))
  }
  x
})

# tt is elapsed time, supported by source check_TS.R:19-23 and analysis.R:143.
# Keep the stored values untouched; diff(tt) supplies derived spacings.
same_grid <- identical(objects[[1L]]$tt, objects[[2L]]$tt)
stopifnot(same_grid)
summary <- do.call(rbind, lapply(seq_along(objects), function(i) {
  x <- objects[[i]]
  spacing <- diff(x$tt) * 1000  # Myr -> kyr
  data.frame(
    taxon = x$taxon, archive_member = members[i], samples = x$nsamp,
    traits = x$nvar, specimen_sum = sum(x$nn), n_min = min(x$nn),
    n_median = median(x$nn), n_max = max(x$nn), samples_n_lt_20 = sum(x$nn < 20),
    elapsed_span_kyr = diff(range(x$tt)) * 1000,
    spacing_min_kyr = min(spacing), spacing_median_kyr = median(spacing),
    spacing_max_kyr = max(spacing), identical_stored_grid = same_grid,
    finite_values_and_covariance_checks = TRUE,
    stringsAsFactors = FALSE
  )
}))
write.table(summary, output, sep = "\t", quote = FALSE, row.names = FALSE)
cat("Two source objects inspected; summary written to", output, "\n")

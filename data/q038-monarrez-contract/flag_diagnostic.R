# Q-038 diagnostic (not a replication): where does range selectivity sit relative to the
# mass-extinction flags in the deposited Monarrez et al. 2023 encounter histories?
# For each class and each interval k (occasion k -> k+1), among genera present at k, regress
# "last occurrence at k" (no later occurrence) on standardised range at k. This ignores imperfect
# detection, which the published Pradel CMR models handle; it only locates the selectivity signal.
# Run from the repository root:  Rscript --vanilla data/q038-monarrez-contract/flag_diagnostic.R
e <- new.env()
load("data/raw/monarrez2023/encounter_history_bs_gr_5class_Big5.Rdata", envir = e)
ds <- e$ds
bits <- do.call(rbind, lapply(strsplit(ds$ch, ""), as.integer))
n_occ <- ncol(bits)
last_occ <- apply(bits, 1, function(r) max(which(r == 1)))
flagged <- c(8, 22, 39, 46, 69)    # occasions carrying mass.ext = 1 (first post-extinction stages)
extinction <- flagged - 1          # intervals ending at the flagged occasion: the extinction intervals
events <- c("end-Ordovician", "Late Devonian", "end-Permian", "end-Triassic", "end-Cretaceous")

fit_k <- function(rows, k) {
  present <- rows[bits[rows, k] == 1]
  y <- as.integer(last_occ[present] == k)
  x <- ds[present, paste0("range", k)]
  if (length(present) < 20 || sum(y) < 5 || sum(y) > length(y) - 5) return(c(NA, NA, length(present), sum(y)))
  m <- glm(y ~ x, family = binomial)
  c(coef(m)[2], sqrt(vcov(m)[2, 2]), length(present), sum(y))
}

res <- list()
for (cl in sort(unique(ds$class))) {
  rows <- which(ds$class == cl)
  for (j in seq_along(events)) {
    for (type in c("extinction_interval", "flagged_interval")) {
      k <- if (type == "extinction_interval") extinction[j] else flagged[j]
      f <- fit_k(rows, k)
      res[[length(res) + 1]] <- data.frame(class = cl, event = events[j], type = type, interval_start = k,
                                           slope = round(f[1], 2), se = round(f[2], 2),
                                           present = f[3], last_occurrences = f[4])
    }
  }
  bg <- setdiff(2:(n_occ - 3), c(extinction, flagged))   # exclude the youngest stages (pull of the Recent)
  s <- sapply(bg, function(k) fit_k(rows, k)[1])
  res[[length(res) + 1]] <- data.frame(class = cl, event = "background", type = "background_median",
                                       interval_start = NA, slope = round(median(s, na.rm = TRUE), 2),
                                       se = NA, present = NA, last_occurrences = sum(!is.na(s)))
}
out <- do.call(rbind, res)
write.table(out, "data/q038-monarrez-contract/flag_diagnostic.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
print(out, row.names = FALSE)

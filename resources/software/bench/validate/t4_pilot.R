# Tranche-4 pilot: generator diagnostics only (no estimator is run). Good's u = 1 - occurrence singletons / occurrences.
# Usage: Rscript t4_pilot.R <dir with occ_*.csv.gz and truth_*.csv> <tag>
args <- commandArgs(TRUE)
occ <- read.csv(file.path(args[1], paste0("occ_", args[2], ".csv.gz")))
truth <- read.csv(file.path(args[1], paste0("truth_", args[2], ".csv")))
d <- do.call(rbind, lapply(split(occ, list(occ$rep, occ$bin), drop = TRUE), function(x) {
  f <- table(x$species)
  data.frame(rep = x$rep[1], bin = x$bin[1], occs = nrow(x), observed = length(f), f1 = sum(f == 1), u = 1 - sum(f == 1) / nrow(x))
}))
d <- merge(truth, d, all.x = TRUE)
d$half <- ifelse(d$bin <= 10, "early", "late")
agg <- aggregate(cbind(global, sampled_area, collections, occs, observed, u) ~ half, d, function(v) round(c(mean = mean(v), min = min(v)), 3))
print(agg)
cat("species ever per rep:", tapply(occ$species, occ$rep, max), "\n")
cat("bins with u < 0.5:", sum(d$u < 0.5, na.rm = TRUE), " < 0.6:", sum(d$u < 0.6, na.rm = TRUE), " < 0.7:", sum(d$u < 0.7, na.rm = TRUE), " of", nrow(d), "\n")

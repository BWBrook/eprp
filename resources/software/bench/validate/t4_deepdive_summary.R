# Tranche-4 DeepDive summary (amendments A3, A4 in ../VALIDATION_T4.md): prior-window strata and the per-dataset arm.
# Usage: Rscript t4_deepdive_summary.R <data dir with dd_label> <results dir> [deepdive dir]
suppressPackageStartupMessages(library(jsonlite))
args <- commandArgs(TRUE)
dat <- args[1]; res <- args[2]; ddir <- if (length(args) > 2) args[3] else "deepdive"
others <- c("raw", "range_through", "chao2_divdyn", "chao2_inext", "squares_divdyn", "sqs", "inext_cov")

ini_value <- function(f, key) as.numeric(sub(".*= *", "", grep(paste0("^", key, " *="), readLines(f), value = TRUE)[1]))
lr <- function(v, a, b) log(mean(v[b], na.rm = TRUE) / mean(v[a], na.rm = TRUE))
summ <- function(v) list(mean = mean(v), se = sd(v) / sqrt(length(v)), n = length(v))

metrics <- function(d, e, s) {
  reps <- split(d, d$rep)
  out <- list(
    spearman_median = median(sapply(reps, function(x) suppressWarnings(cor(x[[e]], x$global, method = "spearman", use = "complete.obs")))),
    male_global = median(abs(log(d[[e]] / d$global)), na.rm = TRUE),
    male_dd_label = median(abs(log(d[[e]] / d$dd_label)), na.rm = TRUE),
    mean_log_ratio_global = mean(log(d[[e]] / d$global), na.rm = TRUE),
    mean_log_ratio_dd_label = mean(log(d[[e]] / d$dd_label), na.rm = TRUE))
  if (s %in% c("S", "E")) out$half_bias <- summ(sapply(reps, function(x) lr(x[[e]], 1:10, 11:20) - lr(x$global, 1:10, 11:20)))
  if (s == "M") out$drop_minus_truth <- summ(sapply(reps, function(x) lr(x[[e]], 9:10, 11:12) - lr(x$global, 9:10, 11:12)))
  out
}

one_scen <- function(s) {
  tag <- paste0(s, "_001_020")
  truth <- read.csv(file.path(dat, paste0("truth_", tag, ".csv")))
  d <- merge(merge(truth, read.csv(file.path(res, paste0("est_", s, ".csv")))), read.csv(file.path(res, paste0("deepdive_", s, ".csv"))))
  occ <- read.csv(file.path(dat, paste0("occ_", tag, ".csv.gz")))
  cfg <- file.path(ddir, s, "config_autotuned.ini")
  target <- ini_value(cfg, "target_n_occs"); max_locs <- ini_value(cfg, "maximum_localities_per_bin")
  n_occ <- tapply(occ$species, occ$rep, length)
  locs <- aggregate(coll ~ rep + bin + area, occ, function(v) length(unique(v)))
  max_area_bin <- tapply(locs$coll, locs$rep, max)
  window <- data.frame(rep = as.integer(names(n_occ)), occurrences = as.vector(n_occ), ratio_to_target = as.vector(n_occ) / target,
                       in_window = as.vector(n_occ) >= target / 1.2 & as.vector(n_occ) <= target * 1.2,
                       max_localities_area_bin = as.vector(max_area_bin[names(n_occ)]), exceeds_max_localities = as.vector(max_area_bin[names(n_occ)]) > max_locs)
  inside <- window$rep[window$in_window]
  shared <- list(all = metrics(d, "deepdive", s),
                 in_window = if (length(inside) > 1) metrics(d[d$rep %in% inside, ], "deepdive", s) else NA,
                 out_of_window = if (length(inside) < 19) metrics(d[!d$rep %in% inside, ], "deepdive", s) else NA)
  own_file <- file.path(res, paste0("deepdive_own_", s, ".csv"))
  own <- NULL
  if (file.exists(own_file)) {
    o <- read.csv(own_file); names(o)[names(o) == "deepdive"] <- "deepdive_own"
    d4 <- d[d$rep %in% 1:4, ]
    d4 <- merge(d4, rbind(o, transform(d4[d4$rep == 1, c("rep", "bin", "deepdive")], deepdive_own = deepdive)[, c("rep", "bin", "deepdive_own")]), all.x = TRUE)
    own <- lapply(setNames(c("deepdive_own", "deepdive", others), c("deepdive_own", "deepdive_shared", others)), function(e) metrics(d4, e, s))
  }
  list(target_n_occs = target, maximum_localities_per_bin = max_locs, window = window, shared = shared, replicates_1_to_4 = own,
       dd_label_over_global = mean(d$dd_label / d$global))
}

out <- setNames(lapply(c("S", "E", "M"), one_scen), c("S", "E", "M"))
write_json(out, file.path(res, "t4_deepdive.json"), auto_unbox = TRUE, pretty = TRUE, digits = 6, na = "null")
for (s in names(out)) {
  cat("==", s, " in window:", sum(out[[s]]$window$in_window), "of 20\n")
  str(out[[s]]$shared, max.level = 2, give.attr = FALSE)
}

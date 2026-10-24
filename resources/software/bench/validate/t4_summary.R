# Tranche-4 summary (declared in ../VALIDATION_T4.md): K1, K2, K3 and the characterisation metrics.
# Usage: Rscript t4_summary.R <data dir> <results dir>
suppressPackageStartupMessages(library(jsonlite))
args <- commandArgs(TRUE)
dat <- args[1]; res <- args[2]
estimators <- c("raw", "range_through", "chao2_divdyn", "chao2_inext", "squares_divdyn", "sqs", "inext_cov", "deepdive")
absolute <- c("chao2_divdyn", "chao2_inext", "squares_divdyn", "deepdive", "raw")

load_scen <- function(s) {
  tag <- paste0(s, "_001_020")
  d <- merge(read.csv(file.path(dat, paste0("truth_", tag, ".csv"))), read.csv(file.path(res, paste0("est_", s, ".csv"))))
  dd <- file.path(res, paste0("deepdive_", s, ".csv"))
  d <- if (file.exists(dd)) merge(d, read.csv(dd), all.x = TRUE) else transform(d, deepdive = NA_real_)
  d[order(d$rep, d$bin), ]
}
D <- setNames(lapply(c("S", "E", "M"), load_scen), c("S", "E", "M"))

lr <- function(v, a, b) log(mean(v[b]) / mean(v[a]))
per_rep <- function(d, f) sapply(split(d, d$rep), f)
summ <- function(v) list(mean = mean(v), sd = sd(v), se = sd(v) / sqrt(length(v)), n = length(v))

half_bias <- function(d, e) per_rep(d, function(x) lr(x[[e]], 1:10, 11:20) - lr(x$global, 1:10, 11:20))
drop_m <- function(d, e) per_rep(d, function(x) lr(x[[e]], 9:10, 11:12))
spear <- function(d, e) per_rep(d, function(x) if (all(is.na(x[[e]]))) NA_real_ else
  suppressWarnings(cor(x[[e]], x$global, method = "spearman", use = "complete.obs")))
male <- function(d, e, truth) median(abs(log(d[[e]] / d[[truth]])), na.rm = TRUE)

all_bins <- do.call(rbind, D)
k1 <- with(all_bins, list(max_abs_diff = max(abs(squares_divdyn - squares_ref), na.rm = TRUE),
                          na_mismatch = sum(is.na(squares_divdyn) != is.na(squares_ref)),
                          n_bins = nrow(all_bins), n_na = sum(is.na(squares_ref))))
k1$pass <- k1$max_abs_diff <= 1e-9 && k1$na_mismatch == 0

k2 <- lapply(c(sqs = "sqs", inext_cov = "inext_cov"), function(e) {
  b <- half_bias(D$S, e); c(summ(b), pass = abs(mean(b)) <= 0.10)
})

bias <- lapply(c(S = "S", E = "E"), function(s) lapply(setNames(estimators, estimators), function(e) summ(half_bias(D[[s]], e))))
truth_half <- lapply(c(S = "S", E = "E"), function(s) summ(per_rep(D[[s]], function(x) lr(x$global, 1:10, 11:20))))
m_truth <- drop_m(D$M, "global")
mass <- c(list(truth_global = summ(m_truth), truth_sampled_area = summ(drop_m(D$M, "sampled_area"))),
          lapply(setNames(estimators, estimators), function(e) { v <- drop_m(D$M, e); c(summ(v), minus_truth = mean(v - m_truth)) }))
spearman <- lapply(D, function(d) lapply(setNames(estimators, estimators), function(e) { v <- spear(d, e); list(median = median(v), min = min(v)) }))
abs_err <- lapply(D, function(d) lapply(setNames(absolute, absolute), function(e)
  list(global = male(d, e, "global"), sampled_area = male(d, e, "sampled_area"),
       mean_log_ratio_global = mean(log(d[[e]] / d$global), na.rm = TRUE),
       dd_label = if ("dd_label" %in% names(d)) male(d, e, "dd_label") else NA,
       mean_log_ratio_dd_label = if ("dd_label" %in% names(d)) mean(log(d[[e]] / d$dd_label), na.rm = TRUE) else NA)))

# K3: both Chao2 variants against independent re-implementations, and their difference
k3_ref <- with(all_bins, {
  S <- raw; T <- collections
  divdyn <- S + (S - 1) / S * f1 * (f1 - 1) / (2 * (f2 + 1))
  inext <- ifelse(f2 > 0, S + (T - 1) / T * f1^2 / (2 * f2), S + (T - 1) / T * f1 * (f1 - 1) / 2)
  list(divdyn_max_abs_diff = max(abs(chao2_divdyn - divdyn)), inext_max_abs_diff = max(abs(chao2_inext - inext)),
       rel_diff_median = median((chao2_divdyn - chao2_inext) / chao2_inext),
       rel_diff_range = range((chao2_divdyn - chao2_inext) / chao2_inext))
})

dd_test <- lapply(c(S = "S", E = "E", M = "M"), function(s) {
  f <- file.path(res, paste0("deepdive_testset_", s, ".txt"))
  if (file.exists(f)) readLines(f, warn = FALSE) else NA
})
diag <- lapply(D, function(d) list(good_u_min = min(d$good_u), sample_coverage_min = min(d$sample_coverage),
                                   inext_cov_extrapolated = sum(d$inext_cov_t > d$collections, na.rm = TRUE),
                                   sqs_na = sum(is.na(d$sqs)), inext_cov_na = sum(is.na(d$inext_cov)),
                                   global_mean = mean(d$global), sampled_area_mean = mean(d$sampled_area),
                                   dd_label_over_global = if ("dd_label" %in% names(d)) mean(d$dd_label / d$global) else NA))

out <- list(K1 = k1, K2 = k2, K3 = k3_ref, bias_half = bias, truth_half_log_ratio = truth_half,
            mass_extinction = mass, spearman = spearman, abs_log_error = abs_err,
            deepdive_testset = dd_test, diagnostics = diag)
write_json(out, file.path(res, "t4_summary.json"), auto_unbox = TRUE, pretty = TRUE, digits = 6)
tab <- do.call(rbind, lapply(names(D), function(s) do.call(rbind, lapply(estimators, function(e) data.frame(
  scenario = s, estimator = e,
  half_bias = if (s != "M") mean(half_bias(D[[s]], e)) else NA,
  mass_drop_minus_truth = if (s == "M") mass[[e]]$minus_truth else NA,
  spearman_median = spearman[[s]][[e]]$median,
  male_global = if (e %in% absolute) abs_err[[s]][[e]]$global else NA,
  male_sampled_area = if (e %in% absolute) abs_err[[s]][[e]]$sampled_area else NA)))))
write.csv(tab, file.path(res, "t4_table.csv"), row.names = FALSE)
print(tab, digits = 3)
cat("K1 pass:", k1$pass, " K2 pass:", sapply(k2, `[[`, "pass"), "\n")

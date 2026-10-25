# Tranche-4 A5 summary (../VALIDATION_T4.md): K5, the evenness dose-response, scenario C and the geometric Weibull arm.
# Usage: Rscript t4_ext_summary.R <results dir>
suppressPackageStartupMessages(library(jsonlite))
res <- commandArgs(TRUE)[1]
scen <- list(S = c("data_v2", "S", "S"), E075 = c("data_dose/E075", "E", "E075"), E100 = c("data_dose/E100", "E", "E100"),
             E150 = c("data_dose/E150", "E", "E150"), E = c("data_v2", "E", "E"), C = c("data_v2", "C", "C"), M = c("data_v2", "M", "M"))
estimators <- c("raw", "range_through", "chao2_divdyn", "chao2_inext", "squares_divdyn", "sqs", "inext_cov",
                "gw_ml_inc", "gw_ml_abund", "gw_ld_inc", "gw_ld_abund")

load <- function(v) {
  d <- merge(read.csv(file.path(v[1], paste0("truth_", v[2], "_001_020.csv"))), read.csv(file.path(res, paste0("est_", v[3], ".csv"))))
  g <- file.path(res, paste0("est_gw_", v[3], ".csv"))
  if (file.exists(g)) d <- merge(d, read.csv(g)[, -3], all.x = TRUE)
  d[order(d$rep, d$bin), ]
}
D <- lapply(scen, load)

lr <- function(v, a, b) log(mean(v[b], na.rm = TRUE) / mean(v[a], na.rm = TRUE))
summ <- function(v) list(mean = mean(v), se = sd(v) / sqrt(length(v)), n = length(v))
half_bias <- function(d, e, keep = rep(TRUE, nrow(d))) sapply(split(seq_len(nrow(d)), d$rep), function(i) {
  x <- d[i, ]; lr(ifelse(keep[i], x[[e]], NA), 1:10, 11:20) - lr(x$global, 1:10, 11:20) })
metrics <- function(d, e, name) {
  if (!e %in% names(d)) return(NULL)
  out <- list(na_bins = sum(is.na(d[[e]])),
              spearman_median = median(sapply(split(d, d$rep), function(x) suppressWarnings(cor(x[[e]], x$global, method = "spearman", use = "complete.obs"))), na.rm = TRUE),
              male_global = median(abs(log(d[[e]] / d$global)), na.rm = TRUE),
              male_sampled_area = median(abs(log(d[[e]] / d$sampled_area)), na.rm = TRUE),
              mean_log_ratio_global = mean(log(d[[e]] / d$global), na.rm = TRUE))
  if (name == "M") out$drop_minus_truth <- summ(sapply(split(d, d$rep), function(x) lr(x[[e]], 9:10, 11:12) - lr(x$global, 9:10, 11:12)))
  else out$half_bias <- summ(half_bias(d, e))
  out
}
tab <- lapply(names(D), function(s) lapply(setNames(estimators, estimators), function(e) metrics(D[[s]], e, s)))
names(tab) <- names(D)

C <- D$C
k5 <- lapply(c(sqs = "sqs", inext_cov = "inext_cov"), function(e) {
  late_na <- sum(is.na(C$sqs))
  b <- half_bias(C, e)
  r <- list(bias = summ(b), sqs_na_bins = late_na)
  if (late_na == 0 || e == "inext_cov") r$pass <- abs(mean(b)) <= 0.10
  else {
    r$pass <- FALSE; r$status <- "undefined as declared (bins below quorum)"
    complete <- names(which(tapply(C$sqs, C$rep, function(v) all(!is.na(v)))))
    r$post_hoc <- list(complete_replicates = summ(half_bias(C[C$rep %in% complete, ], e)),
                       quorum_bins_only = summ(half_bias(C, e, !is.na(C$sqs))))
  }
  r
})
diag <- lapply(D, function(d) list(good_u_min = min(d$good_u), collections_mean = mean(d$collections),
                                   occurrences_per_bin_late = mean(d$raw[d$bin > 10]), global_mean = mean(d$global)))
k4f <- file.path(res, "t4_gw_k4.json")
out <- list(K4 = if (file.exists(k4f)) fromJSON(k4f) else NA, K5 = k5, metrics = tab, diagnostics = diag)
write_json(out, file.path(res, "t4_ext.json"), auto_unbox = TRUE, pretty = TRUE, digits = 6, na = "null")

flat <- do.call(rbind, lapply(names(tab), function(s) do.call(rbind, lapply(names(tab[[s]]), function(e) {
  m <- tab[[s]][[e]]; if (is.null(m)) return(NULL)
  data.frame(scenario = s, estimator = e, bias = if (s == "M") m$drop_minus_truth$mean else m$half_bias$mean,
             se = if (s == "M") m$drop_minus_truth$se else m$half_bias$se, na_bins = m$na_bins,
             spearman = m$spearman_median, male_global = m$male_global, male_sampled_area = m$male_sampled_area)
}))))
write.csv(flat, file.path(res, "t4_ext_table.csv"), row.names = FALSE)
print(flat, digits = 3)
cat("K5 pass:", sapply(k5, `[[`, "pass"), "\n")

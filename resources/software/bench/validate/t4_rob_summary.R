# Tranche-4 A6 summary (../VALIDATION_T4.md): K6 null control, quorum 0.8, abundance-family robustness.
# Usage: Rscript t4_rob_summary.R <results dir>
suppressPackageStartupMessages(library(jsonlite))
res <- commandArgs(TRUE)[1]
lr <- function(v, a, b) log(mean(v[b], na.rm = TRUE) / mean(v[a], na.rm = TRUE))
summ <- function(v) { v <- v[is.finite(v)]; list(mean = mean(v), se = sd(v) / sqrt(length(v)), n = length(v)) }
bias <- function(d, e) summ(sapply(split(d, d$rep), function(x) lr(x[[e]], 1:10, 11:20) - lr(x$global, 1:10, 11:20)))
male <- function(d, e, target) median(abs(log(d[[e]] / d[[target]])), na.rm = TRUE)
load <- function(truth, est, gw = NULL) {
  d <- merge(read.csv(truth), read.csv(file.path(res, est)))
  if (!is.null(gw)) d <- merge(d, read.csv(file.path(res, gw))[, -3], all.x = TRUE)
  d[order(d$rep, d$bin), ]
}

# K6: nothing changes in E050
e050 <- load("data_dose/E050/truth_E_001_020.csv", "est_E050.csv", "est_gw_E050.csv")
k6_est <- c("raw", "chao2_divdyn", "chao2_inext", "squares_divdyn", "sqs", "inext_cov", "gw_ml_inc", "gw_ml_abund")
k6 <- lapply(setNames(k6_est, k6_est), function(e) { b <- bias(e050, e); c(b, pass = abs(b$mean) <= 0.05) })
k6_pass <- all(sapply(k6, `[[`, "pass"))

# quorum 0.8 beside 0.6
q8_dirs <- list(S = "data_v2/truth_S_001_020.csv", C = "data_v2/truth_C_001_020.csv", E = "data_v2/truth_E_001_020.csv",
                E050 = "data_dose/E050/truth_E_001_020.csv", E075 = "data_dose/E075/truth_E_001_020.csv",
                E100 = "data_dose/E100/truth_E_001_020.csv", E150 = "data_dose/E150/truth_E_001_020.csv")
q8 <- lapply(names(q8_dirs), function(x) {
  d8 <- load(q8_dirs[[x]], paste0("est_q08_", x, ".csv")); d6 <- load(q8_dirs[[x]], paste0("est_", x, ".csv"))
  list(sqs_q08 = bias(d8, "sqs"), inext_q08 = bias(d8, "inext_cov"), sqs_q06 = bias(d6, "sqs"), inext_q06 = bias(d6, "inext_cov"),
       sqs_na_q08 = sum(is.na(d8$sqs)), inext_extrapolated_q08 = sum(d8$inext_cov_t > d8$collections, na.rm = TRUE))
})
names(q8) <- names(q8_dirs)

# abundance-family robustness (scenario S's effort fall); the lognormal control at declared effort is S itself
rob_conds <- c(lnorm10 = "S", lnorm4 = "lnorm4", lnormhet10 = "lnormhet10", lnormhet4 = "lnormhet4", gamma10 = "gamma10", gamma4 = "gamma4",
               loguni10 = "loguni10", loguni4 = "loguni4", pareto10 = "pareto10", pareto4 = "pareto4")
rob_est <- c("raw", "chao2_divdyn", "squares_divdyn", "sqs", "inext_cov", "gw_ml_inc")
rob <- lapply(names(rob_conds), function(k) {
  cond <- rob_conds[[k]]
  d <- if (cond == "S") load("data_v2/truth_S_001_020.csv", "est_S.csv", "est_gw_S.csv")
       else load(file.path("data_rob", cond, "truth_S_001_020.csv"), paste0("est_rob_", cond, ".csv"), paste0("est_gw_rob_", cond, ".csv"))
  ok <- !is.na(d$gw_ml_inc) & !is.na(d$chao2_divdyn)
  list(observed_over_global = mean(d$raw / d$global, na.rm = TRUE), collections_mean_early = mean(d$collections[d$bin <= 10]),
       collections_mean_late = mean(d$collections[d$bin > 10]), sampled_over_global = mean(d$sampled_area / d$global),
       gw_na = sum(is.na(d$gw_ml_inc)), sqs_na = sum(is.na(d$sqs)), bins = nrow(d),
       gw_closer_than_chao2 = mean(abs(log(d$gw_ml_inc[ok] / d$sampled_area[ok])) < abs(log(d$chao2_divdyn[ok] / d$sampled_area[ok]))),
       estimators = lapply(setNames(rob_est, rob_est), function(e) list(
         bias = tryCatch(bias(d, e), error = function(err) NA), male_sampled_area = male(d, e, "sampled_area"), male_global = male(d, e, "global"))))
})
names(rob) <- names(rob_conds)

out <- list(K6 = list(pass = k6_pass, estimators = k6), quorum_0.8 = q8, robustness = rob)
write_json(out, file.path(res, "t4_rob.json"), auto_unbox = TRUE, pretty = TRUE, digits = 6, na = "null")
flat <- do.call(rbind, lapply(names(rob), function(k) do.call(rbind, lapply(rob_est, function(e) {
  m <- rob[[k]]$estimators[[e]]
  data.frame(condition = k, estimator = e, bias = if (is.list(m$bias)) m$bias$mean else NA, se = if (is.list(m$bias)) m$bias$se else NA,
             male_sampled_area = m$male_sampled_area, male_global = m$male_global, gw_na = rob[[k]]$gw_na,
             gw_closer = rob[[k]]$gw_closer_than_chao2)
}))))
write.csv(flat, file.path(res, "t4_rob_table.csv"), row.names = FALSE)
print(flat, digits = 3)
cat("K6 pass:", k6_pass, "\n")
print(sapply(q8, function(x) c(sqs08 = x$sqs_q08$mean, inext08 = x$inext_q08$mean, sqs06 = x$sqs_q06$mean, inext06 = x$inext_q06$mean)), digits = 3)

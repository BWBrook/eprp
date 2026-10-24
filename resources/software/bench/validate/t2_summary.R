# Tranche-2 extinction benchmark: score every method (../VALIDATION_T2.md).
# Usage: Rscript t2_summary.R <dir>
suppressPackageStartupMessages(library(jsonlite))
d <- commandArgs(TRUE)[1]
binom99 <- function(N) qbinom(c(0.005, 0.995), N, 0.95) / N

score_arm <- function(arm) {
  x <- read.delim(file.path(d, paste0("t2_extinction_", arm, ".tsv")))
  dropped <- sum(x$dropped == 1)
  x <- x[x$dropped == 0, ]
  te <- x$te_fwd
  gb_lo <- pmin(x$griwm_b_q025_fwd, x$griwm_b_q975_fwd); gb_hi <- pmax(x$griwm_b_q025_fwd, x$griwm_b_q975_fwd)
  gu_lo <- pmin(x$griwm_u_q025_fwd, x$griwm_u_q975_fwd); gu_hi <- pmax(x$griwm_u_q025_fwd, x$griwm_u_q975_fwd)
  covered <- list(
    tbea_ss = te <= x$tbea_ss_upper,
    tbea_marshall = te <= x$tbea_marshall_upper,
    ede_ss = te <= x$ede_ss_upper,
    ede_robson = te <= x$ede_robson_upper,
    ede_ole = x$ede_ole_lower <= te & te <= x$ede_ole_upper,
    ede_solow = te <= x$ede_solow_est,
    ede_mcinerny = te <= x$ede_mcinerny_est,
    ede_burgman = te <= x$ede_burgman_est,
    griwm_biased_interval = gb_lo <= te & te <= gb_hi,
    griwm_unbiased_interval = gu_lo <= te & te <= gu_hi,
    griwm_biased_median_as_bound = te <= x$griwm_b_med,
    agnostic_95 = x$ag_true_bin <= x$ag_bin95)
  est <- list(ede_ss = x$ede_ss_est, ede_robson = x$ede_robson_est, ede_ole = x$ede_ole_est, ede_solow = x$ede_solow_est,
              ede_mcinerny = x$ede_mcinerny_est, ede_burgman = x$ede_burgman_est,
              griwm_biased = x$griwm_b_med, griwm_unbiased = x$griwm_u_med)
  strata <- cut(x$n, c(2, 5, 10, Inf), labels = c("3-5", "6-10", ">10"))
  out <- list(cases = nrow(x), dropped = dropped, binomial99_for_0.95 = binom99(nrow(x)))
  out$methods <- lapply(names(covered), function(m) {
    v <- covered[[m]]
    s <- list(n_scored = sum(!is.na(v)), n_na = sum(is.na(v)), coverage = mean(v, na.rm = TRUE),
              by_fossils = as.list(tapply(v, strata, mean, na.rm = TRUE)))
    if (arm == "B") s$by_te_class <- as.list(tapply(v, x$te_class, mean, na.rm = TRUE))
    s
  })
  names(out$methods) <- names(covered)
  out$point_estimates <- lapply(est, function(e) {
    rel <- (e - te) / x$range
    list(n = sum(!is.na(rel)), median_error_over_range = median(rel, na.rm = TRUE),
         median_abs_error_over_range = median(abs(rel), na.rm = TRUE), frac_before_truth = mean(e < te, na.rm = TRUE))
  })
  out$last_occurrence_gap_over_range <- median((te - x$last) / x$range)
  if (arm == "B") out$te_class_counts <- as.list(table(x$te_class))
  agree <- abs(x$tbea_ss_upper - x$ede_ss_upper)
  agree_d <- abs(x$tbea_ss_upper_disc - x$ede_ss_upper)
  out$ss_agreement <- list(frac_within_0.02 = mean(agree <= 0.02, na.rm = TRUE), max_abs_diff = max(agree, na.rm = TRUE),
                           median_abs_diff = median(agree, na.rm = TRUE),
                           discretised_max_abs_diff = max(agree_d, na.rm = TRUE),
                           discretised_frac_within_1e6 = mean(agree_d <= 1e-6, na.rm = TRUE))
  p <- file.path(d, paste0("t2_agnostic_post_", arm, ".tsv"))
  if (file.exists(p)) {
    a <- read.delim(p)
    a <- a[a$post > 0 & a$post < 1, ]
    dec <- cut(a$post, seq(0, 1, 0.1), include.lowest = TRUE)
    out$agnostic_calibration <- lapply(split(a, dec), function(z) list(n = nrow(z), mean_post = mean(z$post), frac_extinct = mean(z$extinct_by_bin)))
  }
  out
}

res <- lapply(c(A = "A", B = "B", C = "C"), score_arm)
A <- res$A
ci <- A$binomial99_for_0.95
res$E4_pass <- list(
  tbea_ss_coverage_in_99 = A$methods$tbea_ss$coverage >= ci[1] && A$methods$tbea_ss$coverage <= ci[2],
  ede_ss_coverage_in_99 = A$methods$ede_ss$coverage >= ci[1] && A$methods$ede_ss$coverage <= ci[2],
  ss_agreement_99pct = A$ss_agreement$frac_within_0.02 >= 0.99)
res$E4_pass$pass <- all(unlist(res$E4_pass))
write_json(res, file.path(d, "t2_extinction_summary.json"), auto_unbox = TRUE, digits = 5, pretty = TRUE)
for (arm in c("A", "B", "C")) {
  cat("\n== arm", arm, "cases", res[[arm]]$cases, "dropped", res[[arm]]$dropped, "\n")
  for (m in names(res[[arm]]$methods)) cat(sprintf("  %-30s coverage %.3f  (n %d, NA %d)\n", m, res[[arm]]$methods[[m]]$coverage,
                                                   res[[arm]]$methods[[m]]$n_scored, res[[arm]]$methods[[m]]$n_na))
}
cat("\nE4 pass:", toJSON(res$E4_pass, auto_unbox = TRUE), "\n")

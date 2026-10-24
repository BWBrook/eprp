# Tranche-2 follow-up checks after the independent review (../VALIDATION_T2.md A2).
# Usage: Rscript t2_checks.R <outdir>
suppressPackageStartupMessages({library(tbea); library(admtools); library(jsonlite)})
outdir <- commandArgs(TRUE)[1]
res <- list()

# Marshall (1994) in tbea: smallest number of gaps with an upper bracket at quantile 0.95, confidence 0.95
ub <- lapply(2:150, function(N) suppressWarnings(tryCatch(tbea:::.upperBound(0.95, N, 0.95), error = function(e) NA)))
ok <- vapply(ub, function(v) is.numeric(v) && length(v) == 1 && !is.na(v), logical(1))   # the failure branch returns warning text
res$marshall <- list(min_gaps_with_upper = (2:150)[which(ok)[1]],
                     n73 = suppressWarnings(stratCI(sort(runif(73)), method = "Marshall94", confidence = 0.95, quantile = 0.95)),
                     n111 = suppressWarnings(stratCI(sort(runif(111)), method = "Marshall94", confidence = 0.95, quantile = 0.95)))

# admtools on the S1 model: dense-model error count, errors just above each hiatus, and the other hiatus modes
tp_t <- c(0, 4, 6, 12, 15, 21, 24, 30); tp_h <- c(0, 8, 8, 14, 14, 26, 32, 38)
adm <- tp_to_adm(t = tp_t, h = tp_h)
set.seed(901); t <- runif(10000, 0, 30)
dense_t <- seq(0, 30, by = 0.01)
adm_d <- tp_to_adm(t = dense_t, h = time_to_strat(dense_t, adm, destructive = FALSE))
hd <- time_to_strat(t, adm_d, destructive = TRUE); okd <- !is.na(hd)
errd <- abs(strat_to_time(hd[okd], adm_d) - t[okd])
probe <- c(6.001, 6.005, 15.001, 15.005)
res$dense <- list(n_deposited = sum(okd), n_wrong = sum(errd > 1e-9), max_error = max(errd),
                  probe_times = probe,
                  probe_errors = abs(strat_to_time(time_to_strat(probe, adm_d), adm_d) - probe))
heights <- c(2, 4, 8, 9, 11, 14, 15, 20)            # below, at and above the two hiatus surfaces (8 m, 14 m)
truth <- c(1, 2, NA, 7, 9, NA, 15.5, 18)             # analytic times; NA at the surfaces
res$modes <- list(heights = heights, analytic_time = truth,
                  start = get_time(adm, heights, hiat_mode = "start"),
                  end = get_time(adm, heights, hiat_mode = "end"),
                  destroy = get_time(adm, heights, hiat_mode = "destroy"))
write_json(res, file.path(outdir, "t2_checks.json"), auto_unbox = TRUE, digits = 6, pretty = TRUE, na = "null")
cat(toJSON(res, auto_unbox = TRUE, digits = 4, pretty = TRUE, na = "null"), "\n")

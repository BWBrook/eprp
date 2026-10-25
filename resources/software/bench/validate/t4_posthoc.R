# Tranche-4 post hoc checks (amendment A2 in ../VALIDATION_T4.md): K2 variants when SQS misses its quorum.
# Usage: Rscript t4_posthoc.R <data dir> <results dir>
suppressPackageStartupMessages(library(jsonlite))
args <- commandArgs(TRUE)
d <- merge(read.csv(file.path(args[1], "truth_S_001_020.csv")), read.csv(file.path(args[2], "est_S.csv")))
d <- d[order(d$rep, d$bin), ]
lr <- function(v, a, b) log(mean(v[b], na.rm = TRUE) / mean(v[a], na.rm = TRUE))
bias <- function(x, e, keep) lr(ifelse(keep, x[[e]], NA), 1:10, 11:20) - lr(x$global, 1:10, 11:20)
reps <- split(d, d$rep)
complete <- names(reps)[sapply(reps, function(x) all(!is.na(x$sqs)))]
summ <- function(v) list(mean = mean(v), se = sd(v) / sqrt(length(v)), n = length(v))
out <- lapply(c(sqs = "sqs", inext_cov = "inext_cov"), function(e) list(
  complete_replicates = summ(sapply(reps[complete], function(x) bias(x, e, rep(TRUE, nrow(x))))),
  quorum_bins_only = summ(sapply(reps, function(x) bias(x, e, !is.na(x$sqs))))))
ext <- d$inext_cov_t / d$collections
out$inext_extrapolation <- list(bins_extrapolated = sum(ext > 1), beyond_double = sum(ext > 2), max_ratio = max(ext),
                                worst = d[which.max(ext), c("rep", "bin", "collections", "raw", "inext_cov", "inext_cov_t", "global")])
out$incomplete_replicates <- setdiff(names(reps), complete)
write_json(out, file.path(args[2], "t4_posthoc.json"), auto_unbox = TRUE, pretty = TRUE, digits = 6)
print(toJSON(out, auto_unbox = TRUE, pretty = TRUE, digits = 4))

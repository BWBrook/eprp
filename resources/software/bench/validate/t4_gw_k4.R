# Tranche-4 K4 (amendment A5 in ../VALIDATION_T4.md): does richness recover R under its own model?
# Usage: Rscript t4_gw_k4.R <results dir>
suppressPackageStartupMessages({library(richness); library(jsonlite)})
res <- commandArgs(TRUE)[1]
R <- 300
sets <- list(default = c(l = 1, g = 2), moderate = c(l = 0.1, g = 1))
fit <- function(f, n) tryCatch(suppressWarnings(f(n)$richness), error = function(e) NA_real_)
out <- lapply(names(sets), function(k) {
  pr <- sets[[k]]
  v <- do.call(rbind, parallel::mclapply(1:100, function(i) {
    set.seed(44000 + 1000 * match(k, names(sets)) + i)
    x <- rcegs(R, pr[["l"]], pr[["g"]])
    n <- x[x > 0]
    c(S = length(n), ml = fit(cegsML, n), ld = fit(cegsLD, n))
  }, mc.cores = as.integer(Sys.getenv("BENCH_CORES", "12"))))
  s <- function(e) {
    lr <- log(v[, e] / R)
    list(median_log_ratio = median(lr, na.rm = TRUE), mean_log_ratio = mean(lr, na.rm = TRUE),
         iqr = unname(diff(quantile(lr, c(0.25, 0.75), na.rm = TRUE))), na = sum(is.na(lr)),
         pass = abs(median(lr, na.rm = TRUE)) <= 0.10 && sum(is.na(lr)) <= 10)
  }
  list(lambda = pr[["l"]], gamma = pr[["g"]], R = R, observed_fraction = mean(v[, "S"]) / R, ML = s("ml"), LD = s("ld"))
})
names(out) <- names(sets)
write_json(out, file.path(res, "t4_gw_k4.json"), auto_unbox = TRUE, pretty = TRUE, digits = 6)
print(toJSON(out, auto_unbox = TRUE, pretty = TRUE, digits = 4))

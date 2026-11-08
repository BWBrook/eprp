args <- commandArgs(TRUE)
outdir <- args[1]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
suppressPackageStartupMessages({library(admtools); library(fossilbrush); library(Rextinct); library(jsonlite)})
hash_fun <- function(f) {
  p <- tempfile()
  writeLines(deparse(f, width.cutoff = 500L), p)
  h <- strsplit(system2("sha256sum", p, stdout = TRUE), " ")[[1]][1]
  unlink(p)
  h
}
hash_input <- function(x) {
  p <- tempfile()
  writeLines(toJSON(x, auto_unbox = TRUE, digits = 15), p)
  h <- strsplit(system2("sha256sum", p, stdout = TRUE), " ")[[1]][1]
  unlink(p)
  h
}
write_result <- function(x, name) write_json(x, file.path(outdir, name), pretty = TRUE, auto_unbox = TRUE, digits = 15, na = "null")
versions <- lapply(c("admtools", "fossilbrush", "Rextinct"), function(p) {
  d <- packageDescription(p)
  list(package = p, version = d$Version, remote_sha = if (is.null(d$RemoteSha)) NA_character_ else d$RemoteSha)
})
write_result(list(R = R.version.string, locale = Sys.getlocale(), RNGkind = RNGkind(), packages = versions,
  function_sha256 = list(strat_to_time = hash_fun(admtools::strat_to_time),
    get_time_adm = hash_fun(getS3method("get_time", "adm")),
    flag_ranges = hash_fun(fossilbrush::flag_ranges), griwm = hash_fun(Rextinct::griwm))), "package_environment.json")

tp_t <- c(0, 4, 6, 12, 15, 21, 24, 30)
tp_h <- c(0, 8, 8, 14, 14, 26, 32, 38)
inverse <- function(h) vapply(h, function(x) {
  seg <- which(diff(tp_h) > 0 & x > head(tp_h, -1) & x < tail(tp_h, -1))
  if (length(seg) != 1) return(NA_real_)
  i <- seg[1]
  tp_t[i] + (x - tp_h[i]) * (tp_t[i+1] - tp_t[i]) / (tp_h[i+1] - tp_h[i])
}, numeric(1))
forward <- function(t) vapply(t, function(x) {
  i <- max(which(tp_t <= x))
  if (i == length(tp_t)) return(tail(tp_h, 1))
  if (tp_h[i] == tp_h[i+1]) return(NA_real_)
  tp_h[i] + (x - tp_t[i]) * (tp_h[i+1] - tp_h[i]) / (tp_t[i+1] - tp_t[i])
}, numeric(1))
adm <- tp_to_adm(t = tp_t, h = tp_h)
heights <- c(2, 4, 8.001, 9, 11, 14.001, 15, 20, 27, 35)
truth <- inverse(heights)
back <- strat_to_time(heights, adm)
stopifnot(max(abs(time_to_strat(truth, adm) - heights)) < 1e-9)
set.seed(901)
tt <- runif(10000, 0, 30)
hh <- forward(tt)
deposited <- !is.na(hh)
stopifnot(max(abs(hh[deposited] - time_to_strat(tt[deposited], adm))) < 1e-9)
sparse_errors <- abs(strat_to_time(hh[deposited], adm) - tt[deposited])
dense_t <- seq(0, 30, by = 0.01)
dense_adm <- tp_to_adm(t = dense_t, h = time_to_strat(dense_t, adm, destructive = FALSE))
dense_errors <- abs(strat_to_time(hh[deposited], dense_adm) - tt[deposited])
probe_t <- c(6.001, 6.005, 15.001, 15.005)
write_result(list(case = 5, claims = "C096", inputs = list(t = tp_t, h = tp_h, seed = 901),
  input_sha256 = hash_input(list(t = tp_t, h = tp_h, seed = 901)),
  independent_route = "Explicit linear segment algebra; zero-height increments are nondeposition",
  probes = data.frame(height = heights, analytic_time = truth, returned_time = back, error = back - truth),
  n_deposited = sum(deposited), sparse_n_wrong = sum(sparse_errors > 1e-9), sparse_max_error = max(sparse_errors),
  dense_n_wrong = sum(dense_errors > 1e-9), dense_max_random_error = max(dense_errors),
  dense_near_hiatus = data.frame(time = probe_t, error = strat_to_time(forward(probe_t), dense_adm) - probe_t),
  limits = "Two-hiatus synthetic model in admtools 0.7.0. Errors local to affected interpolation segments; later segments are correct. No universal every-height-above-hiatus claim. No StratPal wrapper replay."), "case05_admtools.json")

delta <- c(0, 1, 4.9, 5, 5.1, 6, 9, 9.9, 10, 20, 49.9, 50, 99, 100, 499, 500)
x <- data.frame(genus = "Synthetic", max_ma = 100 + delta, min_ma = 99 + delta)
y <- data.frame(genus = "Synthetic", fad = 100, lad = 80)
f <- flag_ranges(x, y, ycols = c("genus", "fad", "lad"), flag.diff = 5, verbose = FALSE)$occurrence
expected <- delta >= 5
stopifnot(all(f$fad_diff[-1] == delta[-1]))
observed <- f[["fad_flag.5"]] == 1
stopifnot(identical(observed, delta > 0 & as.character(delta) >= "5"), any(expected & !observed))
young <- data.frame(genus = "Synthetic", max_ma = 80.5 - c(1, 5, 10, 30), min_ma = 80 - c(1, 5, 10, 30))
fy <- flag_ranges(young, y, ycols = c("genus", "fad", "lad"), flag.diff = 5, verbose = FALSE)$occurrence
write_result(list(case = 6, claims = "C102", threshold = 5,
  input_sha256 = hash_input(list(x = x, y = y, younger = young, threshold = 5)),
  older_probes = data.frame(delta = delta, numeric_expected = expected, package_flag = observed, returned_difference = f$fad_diff),
  false_negatives = sum(expected & !observed), false_positives = sum(!expected & observed),
  younger_probes = data.frame(true_excess = c(1,5,10,30), returned_difference = fy$lad_diff, package_flag = fy[["lad_flag.5"]]),
  independent_route = "Numeric input-age minus reference-FAD, compared with numeric threshold",
  limits = "Synthetic deterministic grid, not real-world failure prevalence. Character comparison diagnosis applies to fossilbrush 1.0.6; LAD differences additionally include reference range length."), "case06_fossilbrush.json")

ages <- c(1000, 1300, 1800, 2400, 3100, 4000)
nres <- 100L
run_g <- function(sd, biased, caller_seed) {
  input <- tempfile(fileext = ".txt")
  write.table(data.frame(ages, rep(sd, length(ages))), input, row.names = FALSE, col.names = FALSE)
  set.seed(caller_seed)
  result <- suppressMessages(griwm(input, signor_lipps = "ext", biased = biased, resample = nres,
    radiocarbon = 0, calibra = FALSE, alpha = 0.05, resample_save = TRUE))
  after <- runif(5)
  sampled <- read.table("outputGRIWM_resampled_Extinction")[[1]]
  unlink(c(input, "outputGRIWM_resampled_Extinction"))
  list(q = unname(unlist(result$griwm[2, ])), after = after, sampled = sampled)
}
estimate <- function(z, biased) {
  z <- sort(z)
  j <- 2:length(z)
  weights <- 1 / (z[j] - z[1])
  shifts <- if (biased) (z[j] - z[1] + 1) * log(0.05) / j else -(z[j] - z[1] + 1) / j
  round(sum(weights * (z[1] + shifts)) / sum(weights))
}
controls <- lapply(c(TRUE, FALSE), function(b) {
  zero <- run_g(0, b, 721)
  nonzero <- run_g(50, b, 721)
  independent <- vapply(seq_len(nres), function(i) {
    set.seed(i)
    estimate(round(rnorm(length(ages), ages, 50)), b)
  }, numeric(1))
  stopifnot(all(independent == nonzero$sampled), all(zero$q == estimate(ages, b)))
  list(biased = b, zero_sigma_quantiles = zero$q, zero_sigma_independent_point = estimate(ages, b),
    sigma50_quantiles = nonzero$q, independent_resample_max_difference = max(abs(independent - nonzero$sampled)),
    distinct_zero_sigma_resamples = length(unique(zero$sampled)), distinct_sigma50_resamples = length(unique(nonzero$sampled)))
})
a <- run_g(50, TRUE, 721)
b <- run_g(50, TRUE, 829)
set.seed(nres)
invisible(rnorm(length(ages), ages, 50))
predicted_after <- runif(5)
set.seed(721); baseline_a <- runif(5)
set.seed(829); baseline_b <- runif(5)
stopifnot(identical(a$after, b$after), identical(a$after, predicted_after), !identical(baseline_a, baseline_b))
write_result(list(case = 8, claims = c("C110", "C098"), input_ages_BP = ages, resample = nres,
  input_sha256 = hash_input(list(ages_BP = ages, sigma_BP = c(0,50), biased = c(TRUE,FALSE), alpha = 0.05,
    resample = nres, caller_seeds = c(721,829))),
  controls = controls, RNG = list(caller_seeds = c(721,829), next_uniforms_a = a$after, next_uniforms_b = b$after,
    predicted_from_final_iteration = predicted_after, different_seeds_without_call_differ = !identical(baseline_a,baseline_b)),
  independent_route = "Closed-form weighted prefix estimate plus separately coded dating-error draws; caller RNG sentinels",
  limits = "Demonstrates conditional dating-error quantiles and deterministic RNG reset for this input. No fresh population coverage simulation or universal claim about statistical validity. Zero uncertainty is a limiting control; original bench used sigma 0.001 Myr, not zero."), "case08_griwm.json")

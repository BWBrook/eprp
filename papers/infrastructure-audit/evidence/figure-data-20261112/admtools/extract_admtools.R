args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 3L)
out <- args[1]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
suppressPackageStartupMessages({library(admtools); library(jsonlite)})
prior <- read_json(args[2], simplifyVector = TRUE)
prior_env <- read_json(args[3], simplifyVector = TRUE)
sha256 <- function(path) strsplit(system2("sha256sum", path, stdout = TRUE), " ")[[1]][1]
hash_function <- function(fun) {
  path <- tempfile()
  on.exit(unlink(path))
  writeLines(deparse(fun, width.cutoff = 500L), path)
  sha256(path)
}
function_hashes <- list(
  strat_to_time = hash_function(admtools::strat_to_time),
  get_time_adm = hash_function(getS3method("get_time", "adm"))
)
stopifnot(as.character(packageVersion("admtools")) == "0.7.0",
          identical(R.version.string, prior_env$R),
          identical(function_hashes$strat_to_time, prior_env$function_sha256$strat_to_time),
          identical(function_hashes$get_time_adm, prior_env$function_sha256$get_time_adm))
tp_t <- c(0, 4, 6, 12, 15, 21, 24, 30)
tp_h <- c(0, 8, 8, 14, 14, 26, 32, 38)
seed <- 901
stopifnot(identical(tp_t, as.numeric(prior$inputs$t)),
          identical(tp_h, as.numeric(prior$inputs$h)), seed == prior$inputs$seed)
forward <- function(times) vapply(times, function(time) {
  i <- max(which(tp_t <= time))
  if (i == length(tp_t)) return(tail(tp_h, 1))
  if (tp_h[i] == tp_h[i + 1L]) return(NA_real_)
  tp_h[i] + (time - tp_t[i]) * (tp_h[i + 1L] - tp_h[i]) / (tp_t[i + 1L] - tp_t[i])
}, numeric(1))
inverse <- function(heights) vapply(heights, function(height) {
  i <- which(diff(tp_h) > 0 & height > head(tp_h, -1L) & height < tail(tp_h, -1L))
  stopifnot(length(i) == 1L)
  tp_t[i] + (height - tp_h[i]) * (tp_t[i + 1L] - tp_t[i]) / (tp_h[i + 1L] - tp_h[i])
}, numeric(1))
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
set.seed(seed)
times <- runif(10000, 0, 30)
heights <- forward(times)
keep <- !is.na(heights)
model <- tp_to_adm(t = tp_t, h = tp_h)
stopifnot(max(abs(heights[keep] - time_to_strat(times[keep], model))) < 1e-9,
          max(abs(inverse(heights[keep]) - times[keep])) < 1e-12)
estimated <- strat_to_time(heights[keep], model)
error <- estimated - times[keep]
stopifnot(sum(keep) == prior$n_deposited,
          sum(abs(error) > 1e-9) == prior$sparse_n_wrong,
          abs(max(abs(error)) - prior$sparse_max_error) < 1e-12)
tab <- data.frame(draw_index = which(keep), height = heights[keep],
                  truth_time_myr = times[keep], estimated_time_myr = estimated,
                  error_myr = error, deposition_segment = findInterval(heights[keep], unique(tp_h)))
tab <- tab[order(tab$height, tab$draw_index), ]
write_exact <- function(table, path) {
  for (name in names(table)) if (is.double(table[[name]])) table[[name]] <- sprintf("%.17g", table[[name]])
  write.table(table, path, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
}
table_path <- file.path(out, "sparse_curve.tsv")
write_exact(tab, table_path)
write_exact(data.frame(time_myr = tp_t, height = tp_h), file.path(out, "tie_points.tsv"))
saved <- read.delim(table_path)
stopifnot(nrow(saved) == 8282L, sum(abs(saved$error_myr) > 1e-9) == 3972L,
          identical(saved$height, tab$height), identical(saved$error_myr, tab$error_myr),
          max(abs(saved$estimated_time_myr - saved$truth_time_myr - saved$error_myr)) < 1e-14)
script <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)[1])
input_file <- tempfile()
writeLines(toJSON(list(t = tp_t, h = tp_h, seed = seed), auto_unbox = TRUE, digits = 15), input_file)
input_hash <- sha256(input_file)
unlink(input_file)
stopifnot(identical(input_hash, prior$input_sha256))
receipt <- list(
  panel = "Figure 3A", claim = "C096", source_revision = "5c37437",
  method = "Fresh admtools 0.7.0 strat_to_time on the original seed-901 deposited sample; explicit linear-segment truth.",
  sign = "estimated_time_myr minus truth_time_myr",
  environment = list(R = R.version.string, admtools = as.character(packageVersion("admtools")),
                     RNGkind = RNGkind(), function_sha256 = function_hashes,
                     image = "sha256:44432c896c3622e92c68f11716d639745b0fa2b4d6c47124538461389f6daab6"),
  inputs = list(t = tp_t, h = tp_h, seed = seed, random_draws = 10000L,
                input_sha256 = input_hash,
                prior_case = list(file = basename(args[2]), sha256 = sha256(args[2])),
                prior_environment = list(file = basename(args[3]), sha256 = sha256(args[3]))),
  script_sha256 = sha256(script),
  output_sha256 = list(sparse_curve_tsv = sha256(table_path), tie_points_tsv = sha256(file.path(out, "tie_points.tsv"))),
  checks = list(n_deposited = nrow(saved), n_non_deposited = sum(!keep),
                error_tolerance_myr = 1e-9, n_wrong = sum(abs(saved$error_myr) > 1e-9),
                max_abs_error_myr = max(abs(saved$error_myr)), min_signed_error_myr = min(saved$error_myr),
                max_signed_error_myr = max(saved$error_myr),
                full_precision_round_trip = TRUE, independent_linear_segment_truth = TRUE),
  hiatuses = list(height = c(8, 14), time_start_myr = c(4, 12), time_end_myr = c(6, 15)),
  limits = "Sparse two-hiatus synthetic model only. All 8,282 original deposited draws are included, sorted by height; this is not a new regular grid or the dense-model near-hiatus probe. Segment labels permit plotting without joining across hiatus jumps."
)
write_json(receipt, file.path(out, "receipt.json"), auto_unbox = TRUE, pretty = TRUE, digits = 17)
cat("C096: ", nrow(saved), " deposited; ", sum(abs(saved$error_myr) > 1e-9), " wrong; max ",
    sprintf("%.17g", max(abs(saved$error_myr))), " Myr\n", sep = "")

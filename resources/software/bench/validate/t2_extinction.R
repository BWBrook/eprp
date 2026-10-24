# Tranche-2 extinction-date benchmark E4-E6 (../VALIDATION_T2.md).
# Usage: Rscript t2_extinction.R <outdir> [n_cases] [griwm_resample]
suppressPackageStartupMessages({library(paleobuddy); library(EDE); library(tbea); library(Rextinct); library(admtools); library(jsonlite)})
source("/opt/agnostic/agnostic.R")
args <- commandArgs(TRUE)
outdir <- args[1]
n_cases <- if (length(args) > 1) as.integer(args[2]) else 2000
griwm_resample <- if (length(args) > 2) as.integer(args[3]) else 1000
cores <- as.integer(Sys.getenv("BENCH_CORES", "12"))
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
tmax <- 30; unit <- 0.01

# ---- cases (truth) ----
cases <- list(); seed <- 0
while (length(cases) < n_cases) {
  seed <- seed + 1; set.seed(50000 + seed)
  s <- bd.sim(50, 0.3, 0.2, tMax = tmax)
  f <- suppressMessages(sample.clade(s, 1.0, tmax))
  ext <- which(!s$EXTANT)
  for (k in ext) {
    ages <- sort(f$SampT[f$Species == paste0("t", k)], decreasing = TRUE)
    if (length(ages) >= 3) cases[[length(cases) + 1]] <- list(clade_seed = 50000 + seed, species = k, TS = s$TS[k], TE = s$TE[k], ages = ages)
    if (length(cases) >= n_cases) break
  }
}

# ---- estimators ----
na_row <- function(prefix, fields) setNames(rep(NA_real_, length(fields)), paste0(prefix, "_", fields))
safe <- function(expr) tryCatch(suppressWarnings(suppressMessages(expr)), error = function(e) NULL)

run_methods <- function(ages, TE, sigma) {
  fwd <- sort(tmax - ages); te_f <- tmax - TE; n <- length(fwd); R <- max(fwd) - min(fwd)
  out <- c(n = n, range = R, last = max(fwd), te_fwd = te_f)
  ss <- safe(stratCI(fwd, method = "Strauss-Sadler89", nparams = "one.par", C = 0.95, endpoint = "first"))
  out <- c(out, tbea_ss_upper = if (is.null(ss)) NA else unname(ss["maxEst"]))
  mh <- safe(stratCI(fwd, method = "Marshall94", confidence = 0.95, quantile = 0.95))
  out <- c(out, tbea_marshall_upper = if (is.null(mh) || length(mh) < 2) NA else mh[2])
  u <- round(fwd / unit); tab <- table(u)
  ssd <- safe(stratCI(u * unit, method = "Strauss-Sadler89", nparams = "one.par", C = 0.95, endpoint = "first"))
  out <- c(out, tbea_ss_upper_disc = if (is.null(ssd)) NA else unname(ssd["maxEst"]))
  sd <- safe(sighting_data(data.frame(year = as.numeric(names(tab)), sightings = as.integer(tab))))
  ede <- function(fn, ...) {
    r <- if (is.null(sd)) NULL else safe(fn(sd, ...))
    if (is.null(r)) return(c(est = NA, lower = NA, upper = NA))
    c(est = unclass(r)$estimate %||% NA, lower = unclass(r)$lower %||% NA, upper = unclass(r)$upper %||% NA) * unit
  }
  test_year <- round(tmax / unit)
  for (m in list(list("ede_ss", strauss1989), list("ede_robson", robson1964), list("ede_ole", ole))) {
    v <- ede(m[[2]]); names(v) <- paste0(m[[1]], "_", names(v)); out <- c(out, v)
  }
  for (m in list(list("ede_solow", solow1993), list("ede_mcinerny", mcinerny2006), list("ede_burgman", burgman1995))) {
    v <- ede(m[[2]], test_year = test_year); names(v) <- paste0(m[[1]], "_", names(v)); out <- c(out, v)
  }
  gfile <- tempfile(fileext = ".txt")   # griwm reads a file of integer years BP and integer errors
  write.table(data.frame(round(ages * 1e6), round(rep(sigma * 1e6, n))), gfile, col.names = FALSE, row.names = FALSE)
  for (b in c(TRUE, FALSE)) {
    g <- safe(griwm(gfile, signor_lipps = "ext", biased = b, alpha = 0.05,
                    resample = griwm_resample, radiocarbon = 0, calibra = FALSE))
    v <- if (is.null(g)) c(NA, NA, NA) else tmax - as.numeric(g$griwm[2, 1:3]) / 1e6
    names(v) <- paste0(if (b) "griwm_b" else "griwm_u", c("_q025_fwd", "_med", "_q975_fwd"))
    out <- c(out, v)
  }
  b0 <- floor(min(fwd)); bins <- b0:(tmax - 1)
  onoff <- as.integer(bins %in% floor(fwd))
  # agnostic.R fails under R >= 4.3 if `total` is supplied (`||` on a vector); omitting it gives total = 1 per bin
  post <- safe(agnostic(onoff, prior = 0.5))
  if (is.null(post) || all(is.na(post))) {
    out <- c(out, ag_bin95 = NA, ag_true_bin = floor(te_f) - b0 + 2)
  } else {
    i95 <- which(post >= 0.95)[1]
    out <- c(out, ag_bin95 = if (is.na(i95)) Inf else i95, ag_true_bin = floor(te_f) - b0 + 2)
  }
  unlink(gfile)
  list(row = out, post = post)
}
`%||%` <- function(a, b) if (is.null(a) || length(a) == 0) b else a

# hiatus model for arm B (forward time; hiatuses at 3-5, 7-9, 12-14, 17-19, 22-24, 26-28 Ma)
hi <- rbind(c(2, 4), c(6, 8), c(11, 13), c(16, 18), c(21, 23), c(25, 27))
tp <- sort(unique(c(0, as.vector(t(hi)), tmax)))
hgt <- numeric(length(tp)); for (i in 2:length(tp)) hgt[i] <- hgt[i - 1] + if (any(hi[, 1] == tp[i - 1] & hi[, 2] == tp[i])) 0 else (tp[i] - tp[i - 1])
adm_b <- tp_to_adm(t = tp, h = hgt, T_unit = "Myr", L_unit = "m")
te_class <- function(te_f) {
  if (any(te_f > hi[, 1] & te_f < hi[, 2])) return("in_hiatus")
  if (any(te_f >= hi[, 2] & te_f <= hi[, 2] + 1)) return("within_1_after")
  "elsewhere"
}

arm_rows <- function(arm) {
  RNGkind("L'Ecuyer-CMRG"); set.seed(switch(arm, A = 61, B = 62, C = 63))
  res <- parallel::mclapply(seq_along(cases), function(i) {
    cs <- cases[[i]]; ages <- cs$ages; sigma <- 0.001
    if (arm == "B") ages <- ages[!is.na(time_to_strat(tmax - ages, adm_b, destructive = TRUE))]
    if (arm == "C") { ages <- pmin(tmax, pmax(0, ages + rnorm(length(ages), 0, 0.25))); sigma <- 0.25 }
    if (length(ages) < 3) return(list(row = c(case = i, dropped = 1), post = NULL))
    r <- run_methods(ages, cs$TE, sigma)
    list(row = c(case = i, dropped = 0, r$row), post = r$post)
  }, mc.cores = cores)
  rows <- lapply(res, `[[`, "row")
  cols <- unique(unlist(lapply(rows, names)))
  df <- as.data.frame(do.call(rbind, lapply(rows, function(r) r[cols])))
  names(df) <- cols
  if (arm == "B") df$te_class <- vapply(seq_len(nrow(df)), function(i) te_class(tmax - cases[[df$case[i]]]$TE), "")
  posts <- do.call(rbind, lapply(seq_along(res), function(i) {
    p <- res[[i]]$post; if (is.null(p) || all(is.na(p))) return(NULL)
    tb <- df$ag_true_bin[i]
    data.frame(case = df$case[i], bin = seq_along(p), post = p, extinct_by_bin = as.integer(tb <= seq_along(p)))
  }))
  list(df = df, posts = posts)
}

summary_out <- list(meta = list(date = format(Sys.time(), tz = "UTC"), n_cases = length(cases), griwm_resample = griwm_resample,
                                clade_seeds = range(sapply(cases, `[[`, "clade_seed")), cores = cores,
                                packages = as.list(sapply(c("EDE", "tbea", "Rextinct", "admtools", "paleobuddy"), function(p) as.character(packageVersion(p))))))
for (arm in c("A", "B", "C")) {
  t0 <- Sys.time()
  r <- arm_rows(arm)
  write.table(r$df, file.path(outdir, paste0("t2_extinction_", arm, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  if (!is.null(r$posts)) write.table(r$posts, file.path(outdir, paste0("t2_agnostic_post_", arm, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
  summary_out$meta[[paste0("seconds_", arm)]] <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  cat("arm", arm, "done in", format(Sys.time() - t0), "\n")
}
write_json(summary_out, file.path(outdir, "t2_extinction_meta.json"), auto_unbox = TRUE, pretty = TRUE)

# Tranche-2 tests S1-S5 and P1 (../VALIDATION_T2.md).
# Usage: Rscript t2_strat.R <outdir> [p1_reps]
suppressPackageStartupMessages({library(admtools); library(StratPal); library(paleoAM); library(jsonlite)})
args <- commandArgs(TRUE)
outdir <- args[1]
p1_reps <- if (length(args) > 1) as.integer(args[2]) else 200
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
z_ok <- function(z) abs(z) < 3
res <- list(meta = list(date = format(Sys.time(), tz = "UTC"),
                        packages = as.list(sapply(c("admtools", "StratPal", "paleoAM"), function(p) as.character(packageVersion(p))))))

# S1, S2: sparse model with two hiatuses
tp_t <- c(0, 4, 6, 12, 15, 21, 24, 30); tp_h <- c(0, 8, 8, 14, 14, 26, 32, 38)
adm <- tp_to_adm(t = tp_t, h = tp_h, T_unit = "Myr", L_unit = "m")
set.seed(901)
t <- runif(10000, 0, 30)
h <- time_to_strat(t, adm, destructive = TRUE)
back <- strat_to_time(h, adm)
ok <- !is.na(h)
err <- abs(back[ok] - t[ok])
seg <- findInterval(t[ok], tp_t)
res$S1 <- list(n = sum(ok), max_abs_error = max(err), n_wrong = sum(err > 1e-9),
               max_error_by_segment = as.list(tapply(err, paste0(tp_t[seg], "-", tp_t[seg + 1]), max)),
               pass = all(err < 1e-9))
# S1 dense: tie points every 0.01 Myr with the same hiatuses
dense_t <- seq(0, 30, by = 0.01)
dense_h <- time_to_strat(dense_t, adm, destructive = FALSE)
adm_d <- tp_to_adm(t = dense_t, h = dense_h, T_unit = "Myr", L_unit = "m")
hd <- time_to_strat(t, adm_d, destructive = TRUE)
okd <- !is.na(hd)
res$S1_dense <- list(n = sum(okd), max_abs_error = max(abs(strat_to_time(hd[okd], adm_d) - t[okd])), spacing = 0.01)

frac_na <- mean(is.na(h)); exp_na <- 5 / 30
z2 <- (frac_na - exp_na) / sqrt(exp_na * (1 - exp_na) / length(t))
res$S2 <- list(frac_na = frac_na, expected = exp_na, z = z2, completeness = get_completeness(adm),
               hiat_duration = get_hiat_duration(adm),
               pass = z_ok(z2) && abs(get_completeness(adm) - 25 / 30) < 1e-9 && abs(sum(get_hiat_duration(adm)) - 5) < 1e-9)

# S3: constant accumulation
adm3 <- tp_to_adm(t = c(0, 30), h = c(0, 60))
t3 <- runif(1000, 0, 30)
res$S3 <- list(max_abs_error = max(abs(time_to_strat(t3, adm3) - 2 * t3)),
               pass = max(abs(time_to_strat(t3, adm3) - 2 * t3)) < 1e-9)

# S4: p3
set.seed(904)
draws <- lapply(1:20000, function(i) p3(rate = 2, from = 0, to = 10))
cnt <- lengths(draws)
z4 <- (mean(cnt) - 20) / (sd(cnt) / sqrt(length(cnt)))
vr <- var(cnt) / 20; tol4 <- 3 * sqrt(2 / length(cnt))
ks4 <- suppressWarnings(ks.test(unlist(draws), "punif", 0, 10)$p.value)
res$S4 <- list(mean = mean(cnt), z = z4, var_ratio = vr, tol = tol4, ks_p = ks4,
               pass = z_ok(z4) && abs(vr - 1) < tol4 && ks4 > 0.001)

# S5: thin
set.seed(905)
x <- runif(200000, 0, 10)
k1 <- length(thin(x, function(y) rep(0.3, length(y))))
z5 <- (k1 / length(x) - 0.3) / sqrt(0.3 * 0.7 / length(x))
x2 <- thin(x, function(y) y / 10)
ks5 <- suppressWarnings(ks.test(x2, function(q) pmin(1, pmax(0, q^2 / 100)))$p.value)
res$S5 <- list(retained_fraction = k1 / length(x), z = z5, ks_p_linear = ks5, pass = z_ok(z5) && ks5 > 0.001)

# P1: paleoAM mixing
data(gulfOfAlaska)
kde <- getSpeciesSpecificRescaledKDE(gradientOrigDCA = DCA1_GOA, origAbundData = abundData_GOA,
                                     abundanceFloorRatio = 0.5, nBreaksGradientHist = 20, modeledSiteAbundance = 10000)
pocc <- getProbOccViaPresAbs(gradientOrigDCA = DCA1_GOA, origAbundData = abundData_GOA)
g <- seq(min(DCA1_GOA), max(DCA1_GOA), length.out = 30)
set.seed(906)
pool <- t(sapply(seq_len(p1_reps), function(i) {
  m <- getTimestepAbundances(kde, pocc, gradientValues = g, specimensPerTimestep = 10000)
  colSums(m) / sum(m)
}))
mix <- t(sapply(seq_len(p1_reps), function(i) {
  m <- simMixedAssemblageSample(kde, pocc, gradientValues = g, specimensPerTimestep = 10000, nSpecimens = 2000)
  m <- as.numeric(m); m / sum(m)
}))
keep <- colMeans(pool) > 0.01
dif <- colMeans(mix)[keep] - colMeans(pool)[keep]
se <- sqrt(apply(mix[, keep, drop = FALSE], 2, var) / p1_reps + apply(pool[, keep, drop = FALSE], 2, var) / p1_reps)
zp <- dif / se
res$P1 <- list(reps = p1_reps, species_tested = sum(keep), max_abs_z = max(abs(zp)),
               z = as.list(round(zp, 3)), pass = all(abs(zp) < 3.5))

res$pass <- all(c(res$S1$pass, res$S2$pass, res$S3$pass, res$S4$pass, res$S5$pass, res$P1$pass))
write_json(res, file.path(outdir, "t2_strat.json"), auto_unbox = TRUE, digits = 8, pretty = TRUE)
cat(toJSON(res[setdiff(names(res), "meta")], auto_unbox = TRUE, digits = 5, pretty = TRUE), "\n")

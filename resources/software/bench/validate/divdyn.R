# Tranche-1 estimator test E1: divDyn binned rates against lambda*dt and mu*dt (../VALIDATION.md).
# Usage: Rscript divdyn.R <outdir> [n_reps]
suppressPackageStartupMessages({library(paleobuddy); library(divDyn); library(jsonlite)})
args <- commandArgs(TRUE)
outdir <- args[1]
n <- if (length(args) > 1) as.integer(args[2]) else 200
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

lam <- 0.25; mu <- 0.2; tmax <- 40; psi <- 0.5; keep_bins <- 21:38
rates <- c("ext3t", "ori3t", "extGF", "oriGF", "extPC", "oriPC", "extC3t", "oriC3t", "ext2f3", "ori2f3")
bin_of <- function(age) pmin(tmax, floor(tmax - age) + 1)   # bin 1 = oldest (40-39 Ma), higher = younger

one <- function(i) {
  set.seed(7000 + i)
  s <- bd.sim(100, lam, mu, tMax = tmax)
  te <- ifelse(is.na(s$TE), 0, s$TE)
  b0 <- bin_of(s$TS); b1 <- bin_of(pmax(te, 1e-9))
  complete <- do.call(rbind, lapply(seq_along(b0), function(k) data.frame(sp = k, bin = b0[k]:b1[k])))
  f <- suppressMessages(sample.clade(s, psi, tmax))
  sampled <- unique(data.frame(sp = f$Species, bin = bin_of(f$SampT)))
  out <- list()
  for (arm in c("complete", "sampled")) {
    d <- if (arm == "complete") complete else sampled
    x <- divDyn(d, tax = "sp", bin = "bin")
    x <- x[x$bin %in% keep_bins, c("bin", rates)]
    x$rep <- i; x$arm <- arm
    out[[arm]] <- x
  }
  do.call(rbind, out)
}
all <- do.call(rbind, parallel::mclapply(seq_len(n), one, mc.cores = as.integer(Sys.getenv("BENCH_CORES", "12"))))
write.table(all, file.path(outdir, "e1_divdyn_bins.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

truth <- ifelse(startsWith(rates, "ext") | startsWith(rates, "E"), mu, lam)
names(truth) <- rates
summ <- lapply(c("complete", "sampled"), function(arm) {
  a <- all[all$arm == arm, ]
  lapply(rates, function(r) {
    v <- a[[r]]; v <- v[is.finite(v)]
    list(rate = r, truth = unname(truth[r]), mean = mean(v), se = sd(v) / sqrt(length(v)), n = length(v),
         rel_bias = mean(v) / truth[[r]] - 1)
  })
})
names(summ) <- c("complete", "sampled")
declared <- c("ext3t", "ori3t", "extGF", "oriGF", "extPC", "oriPC")
pass <- all(vapply(summ$complete, function(s) if (s$rate %in% declared) abs(s$rel_bias) < 0.05 else TRUE, logical(1)))
res <- list(meta = list(date = format(Sys.time(), tz = "UTC"), n_reps = n, bins = range(keep_bins),
                        packages = list(divDyn = as.character(packageVersion("divDyn")), paleobuddy = as.character(packageVersion("paleobuddy")))),
            complete = summ$complete, sampled = summ$sampled, declared_rates = declared, pass = pass)
write_json(res, file.path(outdir, "e1_divdyn.json"), auto_unbox = TRUE, digits = 6, pretty = TRUE)
cat(toJSON(res, auto_unbox = TRUE, digits = 4, pretty = TRUE), "\n")

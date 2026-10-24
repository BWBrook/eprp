# A2 test G3b (shift order) and the generator timings quoted in the entries.
# Usage: Rscript g3b_timing.R <outdir>
suppressPackageStartupMessages({library(paleobuddy); library(FossilSim); library(TreeSim); library(jsonlite)})
outdir <- commandArgs(TRUE)[1]
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
cores <- as.integer(Sys.getenv("BENCH_CORES", "12"))
RNGkind("L'Ecuyer-CMRG")
set.seed(353)
tmax <- 15; mid <- 15 - 7.5
alive_mid <- unlist(parallel::mclapply(seq_len(2000), function(i) {
  s <- bd.sim(1, c(0.4, 0.1), 0.2, tMax = tmax, lShifts = c(0, 7.5))
  te <- ifelse(is.na(s$TE), 0, s$TE)
  sum(s$TS >= mid & te < mid)
}, mc.cores = cores))
truth <- exp(0.2 * 7.5); reversed <- exp(-0.1 * 7.5)
z <- (mean(alive_mid) - truth) / (sd(alive_mid) / sqrt(length(alive_mid)))

secs <- function(expr) as.numeric(system.time(expr)["elapsed"])
set.seed(1)
sims <- lapply(1:50, function(i) bd.sim(1, 0.3, 0.2, tMax = 15))
trees <- Filter(function(x) inherits(x, "phylo"), sim.bd.age(15, 200, 0.3, 0.2, mrca = FALSE, complete = TRUE))[1:50]
big <- NULL
timing <- list(
  bd_sim_constant_15myr_per_run = secs(lapply(1:200, function(i) bd.sim(1, 0.3, 0.2, tMax = 15))) / 200,
  bd_sim_one_shift_15myr_per_run = secs(lapply(1:20, function(i) bd.sim(1, c(0.4, 0.1), 0.2, tMax = 15, lShifts = c(0, 7.5)))) / 20,
  bd_sim_constant_40myr_n0_100 = secs(big <- bd.sim(100, 0.25, 0.2, tMax = 40)),
  bd_sim_constant_40myr_species = length(big$TS),
  sample_clade_15myr_per_run = secs(for (s in sims) suppressMessages(sample.clade(s, 0.5, 15))) / 50,
  sim_fossils_poisson_per_tree = secs(for (x in trees) sim.fossils.poisson(rate = 0.5, tree = x)) / 50,
  sim_taxonomy_per_tree = secs(for (x in trees) sim.taxonomy(x, beta = 0.5, lambda.a = 0.1)) / 50)

res <- list(G3b = list(n = length(alive_mid), mean_alive_at_7.5 = mean(alive_mid), truth = truth,
                       truth_if_reversed = reversed, z = z, pass = abs(z) < 3),
            timing_seconds = timing, cores = cores, date = format(Sys.time(), tz = "UTC"))
write_json(res, file.path(outdir, "g3b_timing.json"), auto_unbox = TRUE, digits = 6, pretty = TRUE)
cat(toJSON(res, auto_unbox = TRUE, digits = 4, pretty = TRUE), "\n")

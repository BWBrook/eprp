# Post hoc diagnostic for E2 (not a declared test): regenerate the E2 histories
# with the same seeds and compute complete-knowledge rate estimates, (a) from
# all species and (b) from the sampled species only, to separate the effect of
# conditioning on clade size from that of missing unsampled species.
# Usage: Rscript pyrate_attribution.R <outdir>
suppressPackageStartupMessages({library(paleobuddy); library(jsonlite)})
outdir <- commandArgs(TRUE)[1]
dir.create(file.path(outdir, "species_truth"), showWarnings = FALSE)
lam <- 0.3; mu <- 0.2; tmax <- 25
arms <- list(high = list(psi = 1.0, seed0 = 30000, n = 100), low = list(psi = 0.25, seed0 = 40000, n = 50))

est <- function(ts, te, extant, first) {
  d <- sum(ts - te)
  c(lambda = (length(ts) - first) / d, mu = sum(!extant) / d)
}
res <- list()
for (arm in names(arms)) {
  a <- arms[[arm]]
  rows <- t(vapply(seq_len(a$n), function(i) {
    set.seed(a$seed0 + i)    # same stream as pyrate_sim.R
    repeat {
      s <- bd.sim(1, lam, mu, tMax = tmax, nFinal = c(30, 150))
      f <- suppressMessages(sample.clade(s, a$psi, tmax))
      if (length(unique(f$Species)) >= 10) break
    }
    te <- ifelse(is.na(s$TE), 0, s$TE)
    names_all <- paste0("t", seq_along(s$TS))
    sampled <- names_all %in% unique(f$Species)
    all_est <- est(s$TS, te, s$EXTANT, 1)
    smp_est <- est(s$TS[sampled], te[sampled], s$EXTANT[sampled], as.numeric(sampled[1]))
    q_smp <- nrow(f) / sum((s$TS - te)[sampled])
    k <- table(factor(f$Species, levels = names_all))
    write.table(data.frame(species = names_all, ts = s$TS, te = te, k = as.integer(k))[sampled, ],
                file.path(outdir, "species_truth", sprintf("%s_%03d.tsv", arm, i)), sep = "\t", quote = FALSE, row.names = FALSE)
    c(all_est, smp_est, q_sampled = q_smp, n_species = length(s$TS), n_sampled = sum(sampled))
  }, numeric(7)))
  colnames(rows) <- c("lambda_all", "mu_all", "lambda_sampled", "mu_sampled", "q_sampled", "n_species", "n_sampled")
  truth <- c(lambda_all = lam, mu_all = mu, lambda_sampled = lam, mu_sampled = mu, q_sampled = a$psi)
  res[[arm]] <- list(median_rel_bias = as.list(apply(rows[, names(truth)], 2, median) / truth - 1),
                     median_species = median(rows[, "n_species"]), median_sampled = median(rows[, "n_sampled"]))
  write.table(rows, file.path(outdir, paste0("attribution_", arm, ".tsv")), sep = "\t", quote = FALSE, row.names = FALSE)
}
write_json(res, file.path(outdir, "e2_attribution.json"), auto_unbox = TRUE, digits = 5, pretty = TRUE)
cat(toJSON(res, auto_unbox = TRUE, digits = 4, pretty = TRUE), "\n")

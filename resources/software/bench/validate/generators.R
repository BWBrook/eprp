# Tranche-1 generator tests G1-G5 (declared in ../VALIDATION.md).
# Usage: Rscript generators.R <outdir> [scale]; scale < 1 shrinks replicate counts for smoke tests.
suppressPackageStartupMessages({library(paleobuddy); library(FossilSim); library(TreeSim); library(ape); library(jsonlite)})
args <- commandArgs(TRUE)
outdir <- args[1]
scale <- if (length(args) > 1) as.numeric(args[2]) else 1
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
n_rep <- function(n) max(20, round(n * scale))
cores <- as.integer(Sys.getenv("BENCH_CORES", "12"))
RNGkind("L'Ecuyer-CMRG")
rows <- function(X, f) do.call(rbind, parallel::mclapply(X, f, mc.cores = cores))
z_ok <- function(z) abs(z) < 3

lam <- 0.3; mu <- 0.2; tmax <- 15; psi <- 0.5
truth_EN <- exp((lam - mu) * tmax)
truth_surv <- (lam - mu) / (lam - mu * exp(-(lam - mu) * tmax))

# paleobuddy replicates: extant count, species, duration, fossils
set.seed(101)
n1 <- n_rep(20000)
pb <- rows(seq_len(n1), function(i) {
  s <- bd.sim(1, lam, mu, tMax = tmax)
  te <- ifelse(is.na(s$TE), 0, s$TE)
  L <- sum(s$TS - te)
  f <- suppressMessages(sample.clade(s, psi, tmax))
  c(extant = sum(s$EXTANT), species = length(s$TS), L = L, K = nrow(f))
})

# TreeSim trees with FossilSim fossils
set.seed(202)
trees <- sim.bd.age(tmax, n1, lam, mu, mrca = FALSE, complete = TRUE)
tree_summary <- function(tr) {
  if (!inherits(tr, "phylo")) return(c(extant = as.numeric(tr), species = NA, L = NA, K = NA, S = NA, E = NA))
  depth <- node.depth.edgelength(tr)[seq_along(tr$tip.label)] + tr$root.edge
  extant <- sum(abs(depth - tmax) < 1e-6)
  L <- sum(tr$edge.length) + tr$root.edge
  K <- nrow(sim.fossils.poisson(rate = psi, tree = tr))
  c(extant = extant, species = length(tr$tip.label), L = L, K = K, S = tr$Nnode, E = length(tr$tip.label) - extant)
}
ts <- rows(trees, tree_summary)
# sim.bd.age returns 0 for an extinct clade and 1 for a single surviving lineage with no extinct tips
ts[!is.na(ts[, "extant"]) & is.na(ts[, "species"]) & ts[, "extant"] == 1, c("species", "L", "S", "E")] <-
  matrix(c(1, tmax, 0, 0), nrow = 1)[rep(1, sum(!is.na(ts[, "extant"]) & is.na(ts[, "species"]) & ts[, "extant"] == 1)), ]

res <- list(meta = list(date = format(Sys.time(), tz = "UTC"), scale = scale, n = n1, cores = cores,
                        packages = as.list(sapply(c("paleobuddy", "FossilSim", "TreeSim", "ape"), function(p) as.character(packageVersion(p))))))

g1 <- function(extant) {
  m <- mean(extant); se <- sd(extant) / sqrt(length(extant))
  p <- mean(extant > 0); sep <- sqrt(truth_surv * (1 - truth_surv) / length(extant))
  list(mean_extant = m, z_mean = (m - truth_EN) / se, surv = p, z_surv = (p - truth_surv) / sep,
       pass = z_ok((m - truth_EN) / se) && z_ok((p - truth_surv) / sep))
}
res$G1 <- list(truth = list(EN = truth_EN, surv = truth_surv), paleobuddy = g1(pb[, "extant"]), treesim = g1(ts[, "extant"]))

g2 <- function(K, L) {
  keep <- !is.na(K) & L > 0
  K <- K[keep]; L <- L[keep]
  z <- (sum(K) - psi * sum(L)) / sqrt(psi * sum(L))
  disp <- sum((K - psi * L)^2 / (psi * L)) / length(K)
  tol <- 3 * sqrt(2 / length(K))
  list(n = length(K), z = z, dispersion = disp, dispersion_tol = tol, pass = z_ok(z) && abs(disp - 1) < tol)
}
ts_K <- ts[, "K"]
res$G2 <- list(paleobuddy = g2(pb[, "K"], pb[, "L"]), fossilsim = g2(ts_K, ts[, "L"]))

# G3: piecewise speciation, paleobuddy only
set.seed(303)
n3 <- n_rep(20000)
ext3 <- rows(seq_len(n3), function(i) sum(bd.sim(1, c(0.4, 0.1), mu, tMax = tmax, lShifts = c(0, 7.5))$EXTANT))[, 1]
truth3 <- exp(0.2 * 7.5 - 0.1 * 7.5)
z3 <- (mean(ext3) - truth3) / (sd(ext3) / sqrt(n3))
res$G3 <- list(truth = truth3, mean_extant = mean(ext3), z = z3, pass = z_ok(z3))

# G4: surviving replicates, two-sample KS
pb_s <- pb[pb[, "extant"] > 0, , drop = FALSE]
ts_s <- ts[!is.na(ts[, "extant"]) & ts[, "extant"] > 0 & !is.na(ts[, "species"]), , drop = FALSE]
ks <- sapply(c("extant", "species", "L", "K"), function(v) suppressWarnings(ks.test(pb_s[, v], ts_s[, v])$p.value))
res$G4 <- list(n_paleobuddy = nrow(pb_s), n_treesim = nrow(ts_s), ks_p = as.list(ks), pass = all(ks > 0.001),
               note = "KS on discrete counts is conservative (ties)")

# G5: taxonomy on surviving TreeSim trees
set.seed(505)
beta <- 0.5; la <- 0.1
n5 <- n_rep(2000)
alive <- Filter(function(tr) inherits(tr, "phylo"), sim.bd.age(tmax, round(n5 / truth_surv * 1.3), lam, mu, mrca = FALSE, complete = TRUE))
alive <- alive[seq_len(min(n5, length(alive)))]
g5 <- rows(alive, function(tr) {
  tx <- sim.taxonomy(tr, beta = beta, lambda.a = la)
  ends <- tapply(tx$end, tx$sp, min)
  depth <- node.depth.edgelength(tr)[seq_along(tr$tip.label)] + tr$root.edge
  c(orig = length(ends) - 1, term = sum(ends > 1e-6), S = tr$Nnode,
    E = sum(abs(depth - tmax) >= 1e-6), L = sum(tr$edge.length) + tr$root.edge)
})
S <- sum(g5[, "S"]); E <- sum(g5[, "E"]); L <- sum(g5[, "L"])
v <- S * beta * (1 - beta) + la * L
exp_o <- S * (1 + beta) + la * L; exp_t <- E + beta * S + la * L
zo <- (sum(g5[, "orig"]) - exp_o) / sqrt(v); zt <- (sum(g5[, "term"]) - exp_t) / sqrt(v)
res$G5 <- list(n_trees = nrow(g5), originations = sum(g5[, "orig"]), expected_originations = exp_o, z_orig = zo,
               terminations = sum(g5[, "term"]), expected_terminations = exp_t, z_term = zt,
               rates_per_species_time = list(orig = sum(g5[, "orig"]) / L, term = sum(g5[, "term"]) / L),
               pass = z_ok(zo) && z_ok(zt))

res$pass <- all(c(res$G1$paleobuddy$pass, res$G1$treesim$pass, res$G2$paleobuddy$pass, res$G2$fossilsim$pass,
                  res$G3$pass, res$G4$pass, res$G5$pass))
write_json(res, file.path(outdir, "generators.json"), auto_unbox = TRUE, digits = 8, pretty = TRUE)
write.table(pb, file.path(outdir, "g1_paleobuddy.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(ts, file.path(outdir, "g1_treesim.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat(toJSON(res[c("G1", "G2", "G3", "G4", "G5", "pass")], auto_unbox = TRUE, digits = 5, pretty = TRUE), "\n")

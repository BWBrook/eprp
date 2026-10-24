# Tranche-4 generator (declared in ../VALIDATION_T4.md): spatially structured fossil records with known richness.
# Usage: Rscript t4_generate.R <outdir> <scenario S|E|M> <first_rep> <last_rep> [key=value ...]
suppressPackageStartupMessages(library(paleobuddy))
args <- commandArgs(TRUE)
outdir <- args[1]; scen <- args[2]; reps <- as.integer(args[3]):as.integer(args[4])
p <- list(n0 = 400, lambda = 0.05, mu = 0.05, lambda_post = 0.07, survive = 0.4, n_area = 8, geom = 0.5,
          coll_mean = 10, w_sdlog = 0.5, p_empty = 0.15, n_ind = 40, n_late = 12, s_late = 0.3, sd_early = 0.5, sd_late = 2)
for (kv in args[-(1:4)]) { kv <- strsplit(kv, "=")[[1]]; p[[kv[1]]] <- as.numeric(kv[2]) }
tmax <- 100; edges <- seq(tmax, 0, by = -5); nb <- length(edges) - 1
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

lineages <- function() {
  if (scen != "M") {
    s <- bd.sim(p$n0, p$lambda, p$mu, tMax = tmax)
    return(data.frame(ts = s$TS, te = ifelse(is.na(s$TE), 0, s$TE)))
  }
  a <- bd.sim(p$n0, p$lambda, p$mu, tMax = tmax / 2)
  a <- data.frame(ts = a$TS + tmax / 2, te = ifelse(is.na(a$TE), 0, a$TE) + tmax / 2)
  alive <- which(a$te == tmax / 2)
  surv <- alive[runif(length(alive)) < p$survive]
  b <- bd.sim(length(surv), p$lambda_post, p$mu, tMax = tmax / 2)
  b <- data.frame(ts = b$TS, te = ifelse(is.na(b$TE), 0, b$TE))
  a$te[surv] <- b$te[seq_along(surv)]
  rbind(a, b[-seq_along(surv), ])
}

one_rep <- function(r) {
  set.seed(4000 + 1000 * match(scen, c("S", "E", "M", "C")) + r)
  sp <- lineages()
  n <- nrow(sp)
  start <- sample.int(p$n_area, n, replace = TRUE)
  stop <- pmin(p$n_area, start + rgeom(n, p$geom))
  z <- rnorm(n)
  frac <- sapply(seq_len(nb), function(b) pmax(0, pmin(sp$ts, edges[b]) - pmax(sp$te, edges[b + 1])) / 5)
  s_b <- if (scen == "S") rep(c(1, p$s_late), each = nb / 2) else rep(1, nb)
  sd_b <- if (scen == "E") rep(c(p$sd_early, p$sd_late), each = nb / 2) else rep(1, nb)
  n_b <- if (scen == "C") rep(c(p$n_ind, p$n_late), each = nb / 2) else rep(p$n_ind, nb)
  w <- rlnorm(p$n_area, 0, p$w_sdlog)
  n_coll <- matrix(rpois(p$n_area * nb, p$coll_mean * outer(w, s_b)), p$n_area, nb)
  n_coll[runif(length(n_coll)) < p$p_empty] <- 0
  occ <- list(); k <- 0
  for (b in seq_len(nb)) for (a in seq_len(p$n_area)) {
    if (n_coll[a, b] == 0) next
    pool <- which(frac[, b] > 0 & start <= a & stop >= a)
    if (length(pool) == 0) next
    wt <- exp(sd_b[b] * z[pool]) * frac[pool, b]
    for (j in seq_len(n_coll[a, b])) {
      x <- rmultinom(1, n_b[b], wt)[, 1]
      k <- k + 1
      occ[[k]] <- data.frame(rep = r, bin = b, area = a, coll = sprintf("%d_%d_%d", b, a, j), species = pool[x > 0], n = x[x > 0])
    }
  }
  sampled_area <- sapply(seq_len(nb), function(b) {
    open <- which(n_coll[, b] > 0)
    sum(frac[, b] > 0 & sapply(seq_len(n), function(i) any(open >= start[i] & open <= stop[i])))
  })
  truth <- data.frame(rep = r, bin = seq_len(nb), top = edges[-length(edges)], bottom = edges[-1],
                      global = colSums(frac > 0), sampled_area = sampled_area,
                      collections = colSums(n_coll), s_b = s_b, sd_b = sd_b, n_ind = n_b, extant = sum(sp$te == 0),
                      dd_label = colSums(pmin(frac * (stop - start + 1), 1)))
  list(occ = do.call(rbind, occ), truth = truth)
}

res <- parallel::mclapply(reps, one_rep, mc.cores = min(length(reps), as.integer(Sys.getenv("BENCH_CORES", "10"))))
tag <- sprintf("%s_%03d_%03d", scen, min(reps), max(reps))
write.csv(do.call(rbind, lapply(res, `[[`, "occ")), gzfile(file.path(outdir, paste0("occ_", tag, ".csv.gz"))), row.names = FALSE)
write.csv(do.call(rbind, lapply(res, `[[`, "truth")), file.path(outdir, paste0("truth_", tag, ".csv")), row.names = FALSE)
saveRDS(list(params = p, scenario = scen, reps = reps, packages = list(paleobuddy = as.character(packageVersion("paleobuddy")))),
        file.path(outdir, paste0("meta_", tag, ".rds")))

# Tranche-4 estimators (declared in ../VALIDATION_T4.md): raw, range-through, Chao2 (divDyn, iNEXT), squares, SQS, iNEXT coverage.
# Usage: Rscript t4_estimate.R <data dir> <tag> <out csv> [quorum, default 0.6]
suppressPackageStartupMessages({library(divDyn); library(iNEXT)})
args <- commandArgs(TRUE)
occ <- read.csv(file.path(args[1], paste0("occ_", args[2], ".csv.gz")))
q <- if (length(args) > 3) as.numeric(args[4]) else 0.6; nb <- 20

squares_ref <- function(n) {
  S <- length(n); s1 <- sum(n == 1)
  if (s1 == S) NA else S + s1^2 * sum(n^2) / (sum(n)^2 - s1 * S)
}
by_bin <- function(d, col) d[[col]][match(seq_len(nb), d$bin)]

one_rep <- function(x) {
  r <- x$rep[1]
  # divDyn needs character taxa: SQS stops on integer IDs and indices() reads a numeric vector as abundances
  x$species <- paste0("sp", x$species)
  inc <- lapply(split(x, x$bin), function(y) c(length(unique(y$coll)), as.integer(table(y$species))))
  bins <- as.integer(names(inc))
  ix <- t(sapply(split(x$species, x$bin), function(s) indices(s, method = c("chao2", "squares"))[c("chao2", "squares")]))
  chao_inext <- ChaoRichness(inc, datatype = "incidence_freq")
  cov <- estimateD(inc, q = 0, datatype = "incidence_freq", base = "coverage", level = q, nboot = 0)
  info <- DataInfo(inc, datatype = "incidence_freq")
  dd <- divDyn(x, tax = "species", bin = "bin")
  set.seed(7700 + r)
  # divDyn stops when fewer than 3 bins reach the quorum; SQS is then NA for the whole replicate (amendment A6)
  sq <- tryCatch(subsample(x, q = q, tax = "species", bin = "bin", iter = 100, type = "sqs", counter = FALSE),
                 error = function(e) data.frame(bin = seq_len(nb), divSIB = NA_real_))
  est <- data.frame(rep = r, bin = seq_len(nb),
                    raw = by_bin(dd, "divSIB"), range_through = by_bin(dd, "divRT"),
                    sqs = by_bin(sq, "divSIB"))
  per_bin <- data.frame(bin = bins,
                        chao2_divdyn = ix[, 1], squares_divdyn = ix[, 2],
                        squares_ref = sapply(inc, function(v) squares_ref(v[-1])),
                        chao2_inext = chao_inext$Estimator,
                        inext_cov = cov$qD[match(names(inc), cov$Assemblage)],
                        inext_cov_sc = cov$SC[match(names(inc), cov$Assemblage)],
                        inext_cov_t = cov$t[match(names(inc), cov$Assemblage)],
                        sample_coverage = info$SC, collections = info$T,
                        f1 = sapply(inc, function(v) sum(v[-1] == 1)), f2 = sapply(inc, function(v) sum(v[-1] == 2)),
                        good_u = sapply(inc, function(v) 1 - sum(v[-1] == 1) / sum(v[-1])))
  merge(est, per_bin, all.x = TRUE)
}

res <- parallel::mclapply(split(occ, occ$rep), one_rep, mc.cores = as.integer(Sys.getenv("BENCH_CORES", "10")))
bad <- !sapply(res, is.data.frame)
if (any(bad)) stop("replicates failed: ", paste(names(res)[bad], collapse = ", "), "\n", paste(sapply(res[bad], as.character), collapse = "\n"))
write.csv(do.call(rbind, res), args[3], row.names = FALSE)

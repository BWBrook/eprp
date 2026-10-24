# Tranche-1 E2: simulate fossil records with paleobuddy and write PyRate inputs (../VALIDATION.md).
# Usage: Rscript pyrate_sim.R <outdir> <arm: high|low> <n_reps>
suppressPackageStartupMessages({library(paleobuddy); library(jsonlite)})
args <- commandArgs(TRUE)
outdir <- args[1]; arm <- args[2]; n <- as.integer(args[3])
lam <- 0.3; mu <- 0.2; tmax <- 25
psi <- if (arm == "high") 1.0 else 0.25
seed0 <- if (arm == "high") 30000 else 40000
dir.create(file.path(outdir, "inputs"), showWarnings = FALSE, recursive = TRUE)

truth <- list()
for (i in seq_len(n)) {
  set.seed(seed0 + i)
  repeat {
    s <- bd.sim(1, lam, mu, tMax = tmax, nFinal = c(30, 150))
    f <- suppressMessages(sample.clade(s, psi, tmax))
    if (length(unique(f$Species)) >= 10) break
  }
  sp <- unique(f$Species)
  arrays <- vapply(sp, function(x) {
    ages <- sort(f$SampT[f$Species == x], decreasing = TRUE)
    if (f$Extant[f$Species == x][1]) ages <- c(ages, 0)
    paste0("array([", paste(sprintf("%.6f", ages), collapse = ","), "])")
  }, character(1))
  name <- sprintf("%s_%03d", arm, i)
  py <- c("#!/usr/bin/env python", "from numpy import *", "",
          paste0("data_1=[", paste(arrays, collapse = ",\n"), "]"),
          "d=[data_1]", sprintf("names=['%s']", name),
          "def get_data(i): return d[i]", "def get_out_name(i): return names[i]",
          paste0("taxa_names=[", paste0("'", sp, "'", collapse = ","), "]"),
          "def get_taxa_names(): return taxa_names")
  writeLines(py, file.path(outdir, "inputs", paste0(name, ".py")))
  truth[[name]] <- list(lambda = lam, mu = mu, q = psi, seed = seed0 + i, species_total = length(s$TS),
                        species_sampled = length(sp), fossils = nrow(f), extant_sampled = sum(tapply(f$Extant, f$Species, any)))
}
write_json(list(meta = list(date = format(Sys.time(), tz = "UTC"), arm = arm, n = n,
                            paleobuddy = as.character(packageVersion("paleobuddy"))), reps = truth),
           file.path(outdir, paste0("truth_", arm, ".json")), auto_unbox = TRUE, pretty = TRUE)
cat("wrote", n, arm, "inputs\n")

# Tranche-4 DeepDive inputs (declared in ../VALIDATION_T4.md): DeepDiveR input per replicate, config from replicate 1.
# Usage: Rscript t4_deepdive_prep.R <data dir> <tag> <scenario> <out dir>
suppressPackageStartupMessages(library(DeepDiveR))
args <- commandArgs(TRUE)
occ <- read.csv(file.path(args[1], paste0("occ_", args[2], ".csv.gz")))
out <- args[4]
dir.create(out, showWarnings = FALSE, recursive = TRUE)
edges <- seq(100, 0, by = -5)
for (r in sort(unique(occ$rep))) {
  x <- occ[occ$rep == r, ]
  dat <- data.frame(Taxon = paste0("sp", x$species), Region = paste0("A", x$area),
                    MinAge = edges[x$bin + 1], MaxAge = edges[x$bin], Locality = x$coll)
  prep_dd_input(dat, bins = edges, r = 1, age_m = "median", output_file = file.path(out, sprintf("dd_input_%03d.csv", r)))
}
config <- create_config(name = paste0("dd_", args[3]), data_file = "dd_input_001.csv", bins = edges, n_regions = 8)
# Without present diversity, autotune leaves extant_sp = NA and DeepDive 1.0.28 stops parsing it; "0 inf" is bd_simulator's own default
edit_config(config, module = "simulations", parameter = "extant_sp", value = "0 inf")
# The default s_species = 1 starts every training clade from one species; NA lets autotune draw the starting richness (amendment A1)
edit_config(config, module = "simulations", parameter = "s_species", value = "NA")
config$write(file.path(out, "config.ini"))

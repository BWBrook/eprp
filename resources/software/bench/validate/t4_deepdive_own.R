# Tranche-4 per-dataset DeepDive configs (amendment A4 in ../VALIDATION_T4.md): one autotuned config per replicate.
# Usage: Rscript t4_deepdive_own.R <shared scenario dir> <scenario> <out dir> <rep> [<rep> ...]
suppressPackageStartupMessages(library(DeepDiveR))
args <- commandArgs(TRUE)
edges <- seq(100, 0, by = -5)
for (r in as.integer(args[-(1:3)])) {
  out <- file.path(args[3], sprintf("rep_%03d", r))
  dir.create(out, showWarnings = FALSE, recursive = TRUE)
  input <- sprintf("dd_input_%03d.csv", r)
  stopifnot(file.copy(file.path(args[1], input), file.path(out, input), overwrite = TRUE))
  config <- create_config(name = paste0("dd_", args[2]), data_file = input, bins = edges, n_regions = 8)
  edit_config(config, module = "simulations", parameter = "extant_sp", value = "0 inf")
  edit_config(config, module = "simulations", parameter = "s_species", value = "NA")
  config$write(file.path(out, "config.ini"))
}

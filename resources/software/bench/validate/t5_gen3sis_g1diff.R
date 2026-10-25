# Tranche-5 G1 follow-up: what differs in the phylogeny files behind the two failed md5 expectations.
suppressPackageStartupMessages(library(gen3sis))
datapath <- system.file(file.path("extdata", "CaseStudy1"), package = "gen3sis")
config <- create_input_config(file.path(datapath, "config/config_rte.R"))
config$gen3sis$general$start_time <- 5
config$gen3sis$general$end_of_timestep_observer <- function(data, vars, config) {}
setwd(tempdir())
s <- run_simulation(config = config, landscape = file.path(datapath, "landscape"), output_directory = tempdir(), verbose = 0)
for (f in c("phy.txt", "phy.nex")) {
  a <- readLines(file.path(s$parameters$directories$output, f))
  b <- readLines(file.path(datapath, "reference_saves", f))
  cat("==", f, "lines new/ref:", length(a), length(b), " identical:", identical(a, b), "\n")
  n <- max(length(a), length(b))
  for (i in seq_len(n)) if (!identical(a[i], b[i])) cat(sprintf("line %d\n  new: %s\n  ref: %s\n", i, a[i], b[i]))
}
cat("summary all.equal:", isTRUE(all.equal(readRDS(file.path(datapath, "reference_saves", "sgen3sis_summary.rds")), s$summary)), "\n")

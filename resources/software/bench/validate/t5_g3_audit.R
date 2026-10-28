args <- commandArgs(TRUE)
root <- args[1]
nums <- c(1, 2, 8, 10, 12, 13, 15, 16, 18)
deposit <- read.csv(file.path(root, "inputs/zenodo5006413/Data/Data/numerical_values/S3 Data/M1_summary.csv"), check.names = FALSE)
out <- lapply(nums, function(n) {
  work <- file.path(root, "work/g3")
  dir <- file.path(work, "out", paste0("m1_", n), paste0("config_auto_", n))
  source <- read.csv(file.path(work, paste0("g3_m1_", n, ".csv")))
  dep <- deposit[deposit$X == paste0("config_auto_", n), , drop = FALSE]
  stopifnot(nrow(source) == 1, nrow(dep) == 1, source$config == n)
  simulation <- readRDS(file.path(dir, "sgen3sis.rds"))
  species_path <- file.path(dir, "species/species_t_0.rds")
  landscape_path <- file.path(dir, "landscapes/landscape_t_0.rds")
  species <- readRDS(species_path)
  landscape <- readRDS(landscape_path)
  ids <- vapply(species, function(s) as.character(s$id), character(1))
  live <- vapply(species, function(s) any(s$abundance > 0), logical(1))
  cells <- unique(unlist(lapply(species, function(s) names(s$abundance)[s$abundance > 0]), use.names = FALSE))
  stopifnot(!anyDuplicated(ids), length(cells) > 0, all(cells %in% rownames(landscape$environment)))
  alive <- sum(live)
  occupancy <- length(cells) / nrow(landscape$environment)
  phy <- simulation$summary$phylo_summary
  cat(sprintf("config %s: living species=%s; summary=%s; receipt=%s\n", n, alive, phy[nrow(phy), "alive"], source$alive_t0), file = stderr())
  stopifnot(rownames(phy)[nrow(phy)] == "0", as.character(simulation$flag) == as.character(source$flag))
  stopifnot(alive == phy[nrow(phy), "alive"], alive == source$alive_t0)
  stopifnot(length(species) == phy[nrow(phy), "total"], length(species) == source$total)
  stopifnot(isTRUE(all.equal(occupancy, as.numeric(tail(simulation$summary$occupancy, 1)), tolerance = 1e-12)))
  stopifnot(isTRUE(all.equal(occupancy, source$occupancy_final, tolerance = 1e-12)))
  stopifnot(source$seed == dep$seed, source$landscape == dep$landscape, source$deposit_alive_t0 == dep$n_sp_alive_t0)
  data.frame(config = n, seed = dep$seed, landscape = dep$landscape, flag = simulation$flag,
             alive = alive, deposited_alive = dep$n_sp_alive_t0, alive_difference = alive - dep$n_sp_alive_t0,
             occupied_cells = length(cells), habitable_cells = nrow(landscape$environment),
             occupancy = occupancy, deposited_fraction_colonized = dep$fraction_colonized,
             species_md5 = unname(tools::md5sum(species_path)),
             landscape_md5 = unname(tools::md5sum(landscape_path)),
             summary_md5 = unname(tools::md5sum(file.path(dir, "sgen3sis.rds"))))
})
write.table(do.call(rbind, out), file = "", sep = "\t", row.names = FALSE, quote = FALSE)

args <- commandArgs(TRUE)
stopifnot(length(args) == 3)
source_root <- args[1]
work <- args[2]
n <- as.integer(args[3])
stopifnot(!is.na(n))
deposit <- read.csv(file.path(source_root, "inputs/zenodo5006413/Data/Data/numerical_values/S3 Data/M1_summary.csv"), check.names = FALSE)
dep <- deposit[deposit$X == paste0("config_auto_", n), , drop = FALSE]
receipt <- read.csv(file.path(work, paste0("g3_m1_", n, ".csv")))
dir <- file.path(work, "out", paste0("m1_", n), paste0("config_auto_", n))
species_path <- file.path(dir, "species/species_t_0.rds")
landscape_path <- file.path(dir, "landscapes/landscape_t_0.rds")
simulation_path <- file.path(dir, "sgen3sis.rds")
species <- readRDS(species_path)
landscape <- readRDS(landscape_path)
simulation <- readRDS(simulation_path)
stopifnot(nrow(dep) == 1, nrow(receipt) == 1, receipt$config == n)
stopifnot(as.character(simulation$flag) == "OK", as.character(receipt$flag) == "OK")
ids <- vapply(species, function(s) as.character(s$id), character(1))
live <- vapply(species, function(s) any(s$abundance > 0), logical(1))
cells <- unique(unlist(lapply(species, function(s) names(s$abundance)[s$abundance > 0]), use.names = FALSE))
stopifnot(!anyDuplicated(ids), length(cells) > 0, all(cells %in% rownames(landscape$environment)))
alive <- sum(live)
total <- length(species)
occupancy <- length(cells) / nrow(landscape$environment)
phy <- simulation$summary$phylo_summary
stopifnot(rownames(phy)[nrow(phy)] == "0", alive == phy[nrow(phy), "alive"], alive == receipt$alive_t0)
stopifnot(total == phy[nrow(phy), "total"], total == receipt$total)
stopifnot(isTRUE(all.equal(occupancy, as.numeric(tail(simulation$summary$occupancy, 1)), tolerance = 1e-12)))
stopifnot(isTRUE(all.equal(occupancy, receipt$occupancy_final, tolerance = 1e-12)))
stopifnot(isTRUE(all.equal((total - alive) / total, receipt$extinct_fraction, tolerance = 1e-12)))
stopifnot(receipt$seed == dep$seed, receipt$landscape == dep$landscape, receipt$deposit_alive_t0 == dep$n_sp_alive_t0)
result <- data.frame(config = n, seed = dep$seed, landscape = dep$landscape, flag = simulation$flag,
                     alive = alive, deposited_alive = dep$n_sp_alive_t0, alive_difference = alive - dep$n_sp_alive_t0,
                     total_species = total, extinct_fraction = (total - alive) / total,
                     deposited_perc_extinction = dep$perc_extinction, occupied_cells = length(cells),
                     habitable_cells = nrow(landscape$environment), occupancy = occupancy,
                     deposited_fraction_colonized = dep$fraction_colonized,
                     species_md5 = unname(tools::md5sum(species_path)),
                     landscape_md5 = unname(tools::md5sum(landscape_path)),
                     summary_md5 = unname(tools::md5sum(simulation_path)))
write.table(result, file = "", sep = "\t", row.names = FALSE, quote = FALSE)

# Tranche-5 G3 (amendment A3 in ../VALIDATION_T5.md): rerun Hagen et al.'s deposited M1 simulations at gen3sis 1.6.0.
# Usage: Rscript t5_gen3sis_hagen.R compile <landscape: straume_4d|scotese_4d> <deposit Data dir> <work dir>
#        Rscript t5_gen3sis_hagen.R run <config number> <deposit Data dir> <work dir>
#        Rscript t5_gen3sis_hagen.R select <deposit Data dir>
suppressPackageStartupMessages(library(gen3sis))
args <- commandArgs(TRUE)
mode <- args[1]
summary_csv <- function(data_dir) read.csv(file.path(data_dir, "numerical_values", "S3 Data", "M1_summary.csv"), check.names = FALSE)

if (mode == "select") {
  s <- summary_csv(args[2])
  s$n <- as.integer(sub("config_auto_", "", s$X))
  s <- s[order(s$n), ]
  pick <- head(s[s$finished %in% "OK" & s$landscape %in% c("straume_4d", "scotese_4d"), ], 10)
  cat(paste(pick$n, pick$landscape), sep = "\n")
} else if (mode == "compile") {
  # the deposit's compile_gen3sis_landscape.R: water cost function, 8 directions, full distance matrices, 391 steps
  lsname <- args[2]
  ls1 <- readRDS(file.path(args[4], "landscapes_rds", lsname, "landscapes.rds"))
  # the 2020 deposit stores each variable as a data frame (x, y, one column per time step, present first);
  # gen3sis 1.6.0 wants lists of rasters, present first (amendment A4); values are unchanged
  crs <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84"
  ls1 <- lapply(ls1, function(df) lapply(names(df)[-(1:2)], function(cn) raster::rasterFromXYZ(df[, c("x", "y", cn)], crs = crs)))
  cost_function_water <- function(source, habitable_src, dest, habitable_dest) {
    if (!all(habitable_src, habitable_dest)) 2 / 1000 else 1 / 1000
  }
  steps <- paste0(formatC(round(seq(0, 65, length.out = 391), 2), width = 5, flag = "0", digits = 2, format = "f"), "Ma")
  create_input_landscape(landscapes = ls1, cost_function = cost_function_water, directions = 8,
                         output_directory = file.path(args[4], "landscapes", lsname), timesteps = steps,
                         calculate_full_distance_matrices = TRUE,
                         crs = crs, verbose = FALSE)
} else if (mode == "run") {
  n <- as.integer(args[2])
  s <- summary_csv(args[3])
  row <- s[s$X == paste0("config_auto_", n), ]
  cfg <- file.path(args[4], "configs", paste0("config_auto_", n, ".R"))
  out <- file.path(args[4], "out", paste0("m1_", n))
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  setwd(out)
  t0 <- Sys.time()
  sim <- run_simulation(config = cfg, landscape = file.path(args[4], "landscapes", row$landscape), output_directory = out,
                        call_observer = NA, verbose = 0)
  ph <- sim$summary$phylo_summary
  last <- ph[nrow(ph), ]
  occ <- sim$summary$occupancy
  res <- data.frame(config = n, landscape = row$landscape, seed = row$seed, flag = sim$flag,
                    alive_t0 = last[["alive"]], total = last[["total"]], extinct_fraction = (last[["total"]] - last[["alive"]]) / last[["total"]],
                    occupancy_final = unname(occ[length(occ)]),
                    deposit_alive_t0 = row$n_sp_alive_t0, deposit_fraction_colonized = row$fraction_colonized,
                    deposit_perc_extinction = row$perc_extinction, deposit_cpu_time = row$cpu_time,
                    runtime_h = as.numeric(difftime(Sys.time(), t0, units = "hours")))
  write.csv(res, file.path(args[4], paste0("g3_m1_", n, ".csv")), row.names = FALSE)
  print(res)
}

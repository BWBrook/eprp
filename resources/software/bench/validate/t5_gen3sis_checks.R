# Tranche-5 G1, G2a, G2b (amendment A3 in ../VALIDATION_T5.md): gen3sis shipped tests and two closed forms.
# Usage: Rscript t5_gen3sis_checks.R <out json>
suppressPackageStartupMessages({library(gen3sis); library(testthat); library(jsonlite)})
out <- commandArgs(TRUE)[1]
res <- list(gen3sis = as.character(packageVersion("gen3sis")))

# G1: the repository's tests at the 1.6.0 release commit
Sys.setenv(NOT_CRAN = "true")
r <- as.data.frame(test_dir("/opt/src/gen3sis/tests/testthat", reporter = "silent", stop_on_failure = FALSE,
                            package = "gen3sis", load_package = "installed"))
res$G1 <- list(tests = nrow(r), expectations = sum(r$nb), failed = sum(r$failed), errors = sum(r$error),
               skipped = sum(r$skipped), files = unique(r$file), pass = sum(r$failed) == 0 && !any(r$error))

# G2a: one occupied cell, free cells at known distances, Weibull draws
k <- 3; lam <- 700; n_rep <- 4000
d <- seq(100, 1500, by = 200)
cells <- as.character(0:length(d))
dm <- matrix(1e6, length(cells), length(cells), dimnames = list(cells, cells))
dm["0", cells[-1]] <- d; dm[cells[-1], "0"] <- d; diag(dm) <- 0
cfg <- list(gen3sis = list(general = list(trait_names = "dispersal", verbose = 0), initialization = list(initial_abundance = 1),
            dispersal = list(get_dispersal_values = function(n, species, landscape, config) rweibull(n, shape = k, scale = lam))))
land <- list(coordinates = matrix(0, length(cells), 2, dimnames = list(cells, c("x", "y"))))
sp <- gen3sis:::create_species("0", cfg)
set.seed(5001)
hits <- t(replicate(n_rep, cells[-1] %in% names(gen3sis:::disperse(sp, land, dm, cfg)[["abundance"]])))
p <- exp(-(d / lam)^k)
se <- sqrt(pmax(p * (1 - p), 1 / n_rep) / n_rep)
z <- (colMeans(hits) - p) / se
res$G2a <- list(distances = d, expected = p, observed = unname(colMeans(hits)), z = unname(z), pass = all(abs(z) <= 4))

# G2b: two isolated cells, divergence factor 1, threshold 5
thr <- 5
cells2 <- c("1", "2")
dm2 <- matrix(c(0, 5000, 5000, 0), 2, 2, dimnames = list(cells2, cells2))
cfg2 <- list(gen3sis = list(general = list(trait_names = "dispersal", verbose = 0), initialization = list(initial_abundance = 1),
             dispersal = list(get_dispersal_values = function(n, species, landscape, config) rep(1, n)),
             speciation = list(divergence_threshold = thr, get_divergence_factor = function(species, cluster_indices, landscape, config) 1)))
land2 <- list(coordinates = matrix(0, 2, 2, dimnames = list(cells2, c("x", "y"))))
data <- list(all_species = list(gen3sis:::create_species(cells2, cfg2)), landscape = land2, distance_matrix = dm2,
             phy = data.frame(Ancestor = 1, Descendent = 1, Speciation.Time = 100, Extinction.Time = 0, Speciation.Type = "Initial"))
data$all_species[[1]][["id"]] <- "1"
vars <- list(n_sp = 1, n_new_sp_ti = 0, n_sp_added_ti = 0, ti = 99)
n_species <- integer(0)
for (step in 1:(thr + 3)) {
  r2 <- gen3sis:::loop_speciation(cfg2, data, vars)
  data <- r2$data; vars <- r2$vars
  vars$n_sp <- length(data$all_species); vars$n_sp_added_ti <- 0; vars$n_new_sp_ti <- 0; vars$ti <- vars$ti - 1
  n_species[step] <- length(data$all_species)
}
first_split <- which(n_species > 1)[1]
res$G2b <- list(threshold = thr, species_after_each_step = n_species, first_step_with_two = first_split,
                pass = all(n_species[1:thr] == 1) && n_species[thr + 1] == 2)

write_json(res, out, auto_unbox = TRUE, pretty = TRUE, digits = 6)
print(toJSON(res[c("gen3sis", "G1", "G2b")], auto_unbox = TRUE, pretty = TRUE))
cat("G2a pass:", res$G2a$pass, " max |z|:", max(abs(z)), "\n")

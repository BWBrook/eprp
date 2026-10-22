# Profile a Triton RData file (data frames `triton` and `triton.pres`).
# Usage: Rscript triton_profile.R TRITON_RDATA LABEL OUT_TSV [NEPTUNE_ROWS_TSV]
# Writes long-format counts (label, metric, key, value). With NEPTUNE_ROWS_TSV,
# also writes the Neptune-sourced presence rows for record-level linking to NSB.
# Base R only.

args <- commandArgs(trailingOnly = TRUE)
e <- new.env()
load(args[1], envir = e)
label <- args[2]
out <- list()
add <- function(metric, key, value) {
  out[[length(out) + 1]] <<- data.frame(label = label, metric = metric, key = as.character(key),
                                        value = as.character(value))
}
tab <- function(metric, x) {
  t <- table(x, useNA = "ifany")
  keys <- names(t)
  for (i in seq_along(t)) add(metric, ifelse(is.na(keys[i]), "NA", keys[i]), as.integer(t[i]))
}

# Files hold a pair of data frames: <name> (with zero abundances) and <name>.pres.
objs <- ls(e)
add("objects", "", paste(objs, collapse = ","))
pres_name <- grep("\\.pres$", objs, value = TRUE)
stopifnot(length(pres_name) == 1)
all <- get(sub("\\.pres$", "", pres_name), envir = e)
pres <- get(pres_name, envir = e)
col <- function(d, name) if (name %in% names(d)) d[[name]] else rep(NA, nrow(d))
add("rows", "triton (incl. zero abundance)", nrow(all))
add("rows", "triton.pres", nrow(pres))
add("columns", "", paste(names(pres), collapse = ","))

# GTS2020 epoch boundaries (Ma), Triton's scale.
breaks <- c(-Inf, 2.58, 5.333, 23.04, 33.9, 56.0, 66.0, Inf)
labels <- c("Pleistocene-Holocene", "Pliocene", "Miocene", "Oligocene", "Eocene", "Paleocene", "pre-Cenozoic")

if (!"sampleID" %in% names(pres)) pres$sampleID <- col(pres, "triton.SID")
parts <- if ("trim" %in% names(pres)) c("inc", "all") else "all"
for (part in parts) {
  p <- if (part == "inc") pres[pres$trim == "inc", ] else pres
  pre <- paste0(part, ":")
  n_unique <- function(name) length(unique(na.omit(col(p, name))))
  add(paste0(pre, "presence_rows"), "", nrow(p))
  add(paste0(pre, "species"), "", n_unique("species"))
  add(paste0(pre, "orig_species_names"), "", n_unique("orig.species"))
  add(paste0(pre, "samples"), "", n_unique("sampleID"))
  add(paste0(pre, "holes"), "", n_unique("holeID"))
  add(paste0(pre, "sites_with_numeric_site"), "", length(unique(na.omit(suppressWarnings(as.integer(gsub("[^0-9]", "", col(p, "site"))))))))
  add(paste0(pre, "age_min"), "", min(p$age, na.rm = TRUE))
  add(paste0(pre, "age_max"), "", max(p$age, na.rm = TRUE))
  add(paste0(pre, "age_na"), "", sum(is.na(p$age)))
  add(paste0(pre, "pal_lat_na"), "", sum(is.na(p$pal.lat)))
  tab(paste0(pre, "rows_by_epoch"), cut(p$age, breaks, labels, right = FALSE))
  if ("db.source" %in% names(p)) {
    tab(paste0(pre, "rows_by_db_source"), p$db.source)
    for (s in unique(p$db.source)) {
      q <- p[p$db.source == s, ]
      add(paste0(pre, "samples_by_db_source"), s, length(unique(q$sampleID)))
      add(paste0(pre, "holes_by_db_source"), s, length(unique(q$holeID)))
    }
  }
  tab(paste0(pre, "rows_by_age_calc"), col(p, "age.calc"))
  tab(paste0(pre, "rows_by_abun_units"), col(p, "abun.units"))
  tab(paste0(pre, "rows_by_sample_type"), col(p, "sample.type"))
  tab(paste0(pre, "rows_by_abs_latitude_band"), cut(abs(p$latitude), c(0, 30, 60, 90), include.lowest = TRUE))
  tab(paste0(pre, "rows_by_hemisphere"), ifelse(p$latitude >= 0, "N", "S"))
  add(paste0(pre, "rows_age_zero"), "", sum(p$age == 0, na.rm = TRUE))
  add(paste0(pre, "rows_renamed_by_synonymy"), "", sum(as.character(col(p, "species")) != as.character(col(p, "orig.species")), na.rm = TRUE))
}
tab("trim", col(pres, "trim"))
tab("reason", col(pres, "reason"))
add("zero_abundance_rows", "triton minus triton.pres", nrow(all) - nrow(pres))

res <- do.call(rbind, out)
write.table(res, args[3], sep = "\t", quote = FALSE, row.names = FALSE)

if (length(args) >= 4) {
  nep <- pres[pres$db.source == "Neptune", c("sampleID", "holeID", "species", "orig.species", "age", "orig.age",
                                             "age.calc", "round.age", "pal.lat", "sample.depth", "trim",
                                             "abundance", "abun.units")]
  write.table(nep, args[4], sep = "\t", quote = FALSE, row.names = FALSE)
}

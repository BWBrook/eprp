# Profile the data tables in the CRAN GCD package (Global Charcoal Database 4.0.7), globally and for Sahul.
# Usage: Rscript gcd_profile.R UNPACKED_GCD_DIR OUT_TSV
# Sahul regions as in rpd_profile.py. Base R only.

args <- commandArgs(TRUE)
e <- new.env()
rdas <- list.files(file.path(args[1], "data"), pattern = "\\.rda$", full.names = TRUE)
for (f in rdas[!grepl("^PNV_", basename(rdas))]) load(f, envir = e)  # PNV_* are raster layers, not needed
out <- list()
add <- function(table, metric, key, value) out[[length(out) + 1]] <<- data.frame(table, metric, key = as.character(key), value = as.character(value))
tab <- function(table, metric, x, n = 15) {
  t <- sort(table(x, useNA = "ifany"), decreasing = TRUE)
  for (i in seq_len(min(n, length(t)))) add(table, metric, names(t)[i], t[[i]])
}
region <- function(lat, lon) {
  ifelse(!is.na(lon) & lon >= 141 & lon <= 144.5 & lat > -10.6 & lat <= -9, "torres_strait",
  ifelse(!is.na(lat) & lat <= -10.6 & lon >= 112 & lon <= 155, "australia",
  ifelse(!is.na(lon) & lon >= 130.8 & lon <= 156 & lat >= -12 & lat <= 0, "new_guinea", NA)))
}

for (n in sort(ls(e))) add("tables", "rows", n, nrow(get(n, e)))
s <- e$paleofiresites
d <- e$paleofiredata
add("global", "sites", "", nrow(s))
add("global", "samples", "", nrow(d))
tab("global", "sites_by:gcd_version", s$gcd_version)
s$region <- region(s$lat, s$long)
ss <- s[!is.na(s$region), ]
add("sahul", "sites", "", nrow(ss))
tab("sahul", "sites_by:region", ss$region)
tab("sahul", "sites_by:gcd_version", ss$gcd_version)
tab("sahul", "sites_by:country", ss$country)
ds <- d[d$ID_SITE %in% ss$id_site, ]
add("sahul", "samples", "", nrow(ds))
tab("sahul", "samples_by:METHOD", ds$METHOD)
tab("sahul", "samples_by:TYPE", ds$TYPE)
tab("sahul", "samples_by:UNIT", ds$UNIT, 10)
add("sahul", "samples_est_age_missing", "", sum(is.na(ds$EST_AGE)))
mx <- tapply(ds$EST_AGE, ds$ID_SITE, max, na.rm = TRUE)
mx <- mx[is.finite(mx)]
add("sahul", "site_max_est_age_median", "", round(median(mx)))
for (thr in c(20000, 50000)) add("sahul", "sites_max_est_age_ge", thr, sum(mx >= thr))
if (!is.null(e$release)) for (i in seq_len(nrow(e$release))) add("release", "row", i, paste(unlist(e$release[i, ]), collapse = " | "))
write.table(do.call(rbind, out), args[2], sep = "\t", quote = FALSE, row.names = FALSE)

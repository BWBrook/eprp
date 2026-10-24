# Tranche-3 V6, routes (a) and (b): palaeoverse::palaeorotate, point (GPlates Web Service) and grid.
# Usage: Rscript t3_rotate.R <outdir> <pbdb_public_dir> [n_points]
suppressPackageStartupMessages({library(palaeoverse); library(data.table)})
args <- commandArgs(TRUE)
outdir <- args[1]; pdir <- args[2]; n_pts <- if (length(args) > 2) as.integer(args[3]) else 300
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
models <- c("MERDITH2021", "PALEOMAP", "TorsvikCocks2017", "MATTHEWS2016_pmag_ref")
ages <- c(10, 50, 100, 200, 300, 400)

cols <- rbindlist(lapply(Sys.glob(file.path(pdir, "collections__p*.csv")), fread, select = c("collection_no", "lng", "lat")))
cols <- unique(cols[!is.na(lng) & !is.na(lat)])
set.seed(7)
pts <- cols[sample(.N, n_pts)]
fwrite(pts, file.path(outdir, "v6_points.tsv"), sep = "\t")
grid_df <- pts[rep(seq_len(.N), each = length(ages))][, age := rep(ages, times = n_pts)]

point <- rbindlist(lapply(ages, function(a) {
  occ <- as.data.frame(pts[, .(collection_no, lng, lat)]); occ$age <- a
  r <- palaeorotate(occ, model = models, method = "point", uncertainty = FALSE, round = NULL)
  as.data.table(r)
}), fill = TRUE)
fwrite(point, file.path(outdir, "v6_point.tsv"), sep = "\t")

grid <- rbindlist(lapply(models, function(m) {
  r <- as.data.table(palaeorotate(as.data.frame(grid_df), model = m, method = "grid", uncertainty = FALSE))
  r[, model := m]
  r
}), fill = TRUE)
fwrite(grid, file.path(outdir, "v6_grid.tsv"), sep = "\t")
cat("points", nrow(pts), "point rows", nrow(point), "grid rows", nrow(grid), "\n")
cat("point columns:", paste(names(point), collapse = " "), "\ngrid columns:", paste(names(grid), collapse = " "), "\n")

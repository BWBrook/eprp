options(digits = 16)
suppressPackageStartupMessages({library(dggridR); library(sp); library(dplyr); library(ggplot2)})
source("legacy_geometry.R")
source("legacy-dg-process-polydata.R")
stopifnot(as.character(packageVersion("dggridR")) == "3.0.0",
          as.character(packageVersion("iNEXT")) == "3.0.2",
          as.character(packageVersion("sp")) == "2.2.4")
write.table(as.data.frame(installed.packages())[, c("Package", "Version", "Built", "LibPath")],
            "installed-packages.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
capture.output(sessionInfo(), file = "session-info.txt")
capture.output(sf::sf_extSoftVersion(), file = "spatial-libraries.txt")
capture.output(lapply(list(dgconstruct = dgconstruct, dgGEO_to_SEQNUM = dgGEO_to_SEQNUM,
                          dgcellstogrid = dgcellstogrid, estimateD = iNEXT::estimateD), formals),
               file = "api-formals.txt")
grid <- dgconstruct(spacing = 1000, metric = TRUE, resround = "down")
capture.output(str(grid), file = "grid-definition.txt")
points <- data.frame(long = c(0, 179.9, -179.9, 30, 0, 0, 180, -180),
                     lat = c(0, 0, 0, 25, 90, 0, 0, 0))
mapping <- dgGEO_to_SEQNUM(grid, points$long, points$lat)
stopifnot(length(mapping$seqnum) == nrow(points),
          all(is.finite(mapping$seqnum)),
          mapping$seqnum[1] == mapping$seqnum[6],
          mapping$seqnum[7] == mapping$seqnum[8])
write.table(cbind(points, mapping), "synthetic-mapping.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
all_rings <- q027_native_rings(grid, seq_len(dgmaxcell(grid)))
pentagons <- as.integer(names(which(table(all_rings$seqnum) == 6)))
stopifnot(length(pentagons) == 12L)
selected_cells <- sort(unique(c(mapping$seqnum, pentagons[1])))
raw <- q027_native_rings(grid, selected_cells)
native_sf <- dgcellstogrid(dggs = grid, cells = selected_cells)
for (i in seq_len(nrow(native_sf))) {
    r <- raw[raw$seqnum == native_sf$seqnum[i], c("x", "y")]
    xy <- sf::st_coordinates(native_sf[i, ])[, c("X", "Y")]
    stopifnot(isTRUE(all.equal(unname(as.matrix(r)), unname(xy), tolerance = 0)),
              identical(unname(as.numeric(r[1, ])), unname(as.numeric(r[nrow(r), ]))))
}
polygons <- q027_cell_frame(grid, selected_cells)
reference <- dg_process_polydata(raw, frame = TRUE, wrapcells = TRUE)
stopifnot(isTRUE(all.equal(polygons, reference, tolerance = 0)))
stopifnot(all(c("cell", "group", "long", "lat") %in% names(polygons)),
          all(is.finite(polygons$long)), all(is.finite(polygons$lat)),
          all(polygons$long >= -180), all(polygons$long < 360), all(abs(polygons$lat) <= 90 + 1e-8),
          any(polygons$long > 180), any(table(polygons$cell) == 6L))
write.table(polygons, "synthetic-polygons.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
centres <- aggregate(polygons[c("long", "lat")], by = list(cell_id = as.integer(polygons$cell)), FUN = mean)
write.table(centres, "synthetic-cell-means.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
helper_means <- q027_cell_geometry(grid, selected_cells)
stopifnot(isTRUE(all.equal(helper_means$cell_paleolat, centres$lat, tolerance = 0)),
          isTRUE(all.equal(helper_means$cell_paleolng, centres$long, tolerance = 0)))
capture.output(str(mapping), str(native_sf), str(polygons), str(helper_means), file = "geometry-schema.txt")

cases <- list(rarefaction = c(20, 15, 12, 8, 6, 4, 3, 2, 1),
              extrapolation_inside_cap = c(20, 10, 8, 5, 3, rep(1, 4)),
              insufficient_coverage_at_2T = c(20, 10, 8, 5, 3, rep(1, 6)),
              all_singletons = c(20, rep(1, 20)),
              no_singletons = c(20, 20, 20, 20))
results <- lapply(names(cases), function(label) {
    x <- list(site = cases[[label]])
    point <- suppressWarnings(iNEXT::estimateD(x, q = 0, datatype = "incidence_freq",
                                               base = "coverage", level = .9, nboot = 0, conf = .95))
    set.seed(2718)
    bootstrap <- suppressWarnings(iNEXT::estimateD(x, q = 0, datatype = "incidence_freq",
                                                   base = "coverage", level = .9, nboot = 20, conf = .95))
    stopifnot(isTRUE(all.equal(point[c("t", "SC", "qD")], bootstrap[c("t", "SC", "qD")], tolerance = 0)))
    zero_conf <- suppressWarnings(iNEXT::estimateD(x, q = 0, datatype = "incidence_freq",
                                                   base = "coverage", level = .9, nboot = 0, conf = 0))
    stopifnot(isTRUE(all.equal(point[c("t", "SC", "qD")], zero_conf[c("t", "SC", "qD")], tolerance = 0)))
    at_2T <- iNEXT::estimateD(x, q = 0, datatype = "incidence_freq", base = "size",
                            level = 2 * x$site[1], nboot = 0, conf = .95)
    point$case <- label
    point$T <- x$site[1]
    point$SC_at_2T <- at_2T$SC
    point$eligible_2T <- is.finite(point$t) & point$t != 0 & point$t <= 2 * point$T
    point$accepted_qD <- ifelse(point$eligible_2T, point$qD, NA_real_)
    point
})
results <- do.call(rbind, results)
stopifnot(identical(results$eligible_2T, c(TRUE, TRUE, FALSE, FALSE, TRUE)),
          all(results$SC_at_2T[!results$eligible_2T] < .9))
null_error <- tryCatch({iNEXT::estimateD(list(site = cases$rarefaction), q = 0,
                                       datatype = "incidence_freq", base = "coverage", level = .9,
                                       conf = NULL); NA_character_}, error = conditionMessage)
stopifnot(identical(null_error, "arguments imply differing number of rows: 1, 0"))
writeLines(null_error, "conf-null-error.txt")
write.table(results, "synthetic-estimates.tsv", sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
stopifnot(identical(c(0, 40, 40 + 1e-8) != 0 & c(0, 40, 40 + 1e-8) <= 40,
                    c(FALSE, TRUE, FALSE)))
cat("PASS: package pins; deterministic mapping and antimeridian; wrapped polygon schema;\n",
    "coverage point estimates unchanged by bootstrap/conf; 2T eligibility; conf=NULL failure.\n", sep = "")
print(results)

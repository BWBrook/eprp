q027_native_rings <- function(dggs, cells) {
    cells <- unique(cells)
    stopifnot(length(cells) > 0L, all(is.finite(cells)), all(cells >= 1),
              all(cells <= dggridR::dgmaxcell(dggs)))
    as.data.frame(dggridR:::SeqNumGrid(dggs$pole_lon_deg, dggs$pole_lat_deg,
                                     dggs$azimuth_deg, dggs$aperture, dggs$res,
                                     dggs$topology, dggs$projection, cells))
}

q027_cell_frame <- function(dggs, cells) {
    rings <- q027_native_rings(dggs, cells)
    rings <- split(rings, rings$seqnum)
    ids <- names(rings)
    rings <- lapply(rings, function(x) { x["seqnum"] <- NULL; sp::Polygon(x) })
    rings <- lapply(seq_along(rings), function(i) sp::Polygons(list(rings[[i]]), ID = ids[i]))
    polygons <- sp::SpatialPolygons(rings, proj4string = sp::CRS("+proj=longlat +datum=WGS84"))
    frame <- ggplot2::fortify(polygons, region = "seqnum")
    frame$cell <- frame$id
    frame$id <- NULL
    spans <- vapply(split(frame$long, frame$group), function(x) max(x) - min(x), numeric(1))
    wrap <- frame$group %in% names(spans[spans > 180])
    frame$long <- ifelse(wrap, ifelse(frame$long < 0, frame$long + 360, frame$long), frame$long)
    dplyr::arrange(frame, group, order)
}

q027_cell_geometry <- function(dggs, cells) {
    frame <- q027_cell_frame(dggs, cells)
    means <- aggregate(frame[c("lat", "long")], list(cell_id = as.integer(frame$cell)), mean)
    names(means) <- c("cell_id", "cell_paleolat", "cell_paleolng")
    means
}

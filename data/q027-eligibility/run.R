args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("Usage: run.R PREPARATION_DIR GEOMETRY_HELPER OUTPUT_DIR")
prep_dir <- args[[1]]
source(args[[2]])
out_dir <- args[[3]]
if (dir.exists(out_dir)) stop("Output directory already exists")
dir.create(out_dir, recursive = TRUE)
stopifnot(as.character(packageVersion("dggridR")) == "3.0.0",
          as.character(packageVersion("iNEXT")) == "3.0.2")
started <- proc.time()
grid <- dggridR::dgconstruct(spacing = 1000, metric = TRUE, resround = "down")
saveRDS(grid, file.path(out_dir, "grid.rds"))
capture.output(str(grid), file = file.path(out_dir, "grid.txt"))
capture.output(sessionInfo(), file = file.path(out_dir, "session-info.txt"))

write_tsv <- function(x, name) {
  write.table(x, file.path(out_dir, name), sep = "\t", quote = FALSE,
              row.names = FALSE, na = "NA", eol = "\n")
}
mode_region <- function(x) {
  x <- x[!is.na(x) & nzchar(x)]
  if (!length(x)) return(c(region = "UNKNOWN", status = "all_missing"))
  z <- table(x)
  winners <- names(z)[z == max(z)]
  if (length(winners) > 1L) return(c(region = "UNKNOWN", status = "tie"))
  c(region = winners, status = "unique_mode")
}
band <- function(latitude) {
  a <- abs(latitude)
  ifelse(a < 20, "tropical", ifelse(a < 40, "midlatitude", "higher"))
}
estimate <- function(T, frequencies, run) {
  result <- list(qD = NA_real_, t = NA_real_, t_over_T = NA_real_,
                 SC = NA_real_, method = NA_character_,
                 estimator_status = "not_run_le10_rows", warning = "", error = "")
  if (!run) return(result)
  warnings <- character()
  value <- tryCatch(withCallingHandlers(
    iNEXT::estimateD(list(site = c(T, frequencies)), datatype = "incidence_freq",
                    base = "coverage", level = 0.9, q = 0, nboot = 0, conf = 0.95),
    warning = function(w) {
      warnings <<- c(warnings, conditionMessage(w))
      invokeRestart("muffleWarning")
    }), error = function(e) e)
  result$warning <- paste(unique(gsub("[\t\r\n]", " ", warnings)), collapse = " | ")
  if (inherits(value, "error")) {
    result$estimator_status <- "error"
    result$error <- gsub("[\t\r\n]", " ", conditionMessage(value))
    return(result)
  }
  stopifnot(nrow(value) == 1L, value$Order.q == 0,
            all(c("qD", "t", "SC", "Method") %in% names(value)))
  result$qD <- value$qD
  result$t <- value$t
  result$t_over_T <- value$t / T
  result$SC <- value$SC
  result$method <- value$Method
  result$estimator_status <- if (!is.finite(value$qD) || !is.finite(value$t)) {
    "nonfinite"
  } else if (value$t == 0) {
    "t_zero"
  } else if (value$t > 2 * T) {
    "above_2T"
  } else {
    "finite_within_cap"
  }
  result
}

all_cells <- list()
metadata_keys <- c("collection_no", "reference_no", "lithology1",
                   "lithification1", "environment", "cc", "Region")
for (subset in c("original", "dated_public_member")) {
  x <- read.csv(file.path(prep_dir, paste0(subset, ".csv")),
                colClasses = "character", na.strings = "", check.names = FALSE)
  required <- c(metadata_keys, "stage", "plate_model_age", "paleolng", "paleolat",
                "genus", "is_mollusca", "is_excluding_unlithified_pass")
  stopifnot(all(required %in% names(x)), nrow(x) > 0,
            all(x$stage %in% c("Albian", "Campanian")),
            !anyNA(x[c("collection_no", "genus")]))
  for (field in c("paleolng", "paleolat", "plate_model_age")) {
    x[[field]] <- as.numeric(x[[field]])
    stopifnot(all(is.finite(x[[field]])))
  }
  stopifnot(all(abs(x$paleolat) <= 90), all(abs(x$paleolng) <= 180))
  x$cell_id <- as.integer(dggridR::dgGEO_to_SEQNUM(grid, x$paleolng, x$paleolat)$seqnum)
  stopifnot(!anyNA(x$cell_id))
  geometry <- q027_cell_geometry(grid, sort(unique(x$cell_id)))
  stopifnot(!anyDuplicated(geometry$cell_id),
            setequal(geometry$cell_id, x$cell_id),
            all(is.finite(geometry$cell_paleolat)),
            all(abs(geometry$cell_paleolat) <= 90))
  x$cell_paleolat <- geometry$cell_paleolat[match(x$cell_id, geometry$cell_id)]
  x$cell_paleolng <- geometry$cell_paleolng[match(x$cell_id, geometry$cell_id)]
  groups <- split(seq_len(nrow(x)), interaction(x$stage, x$cell_id, drop = TRUE))
  for (indices in groups) {
    z <- x[indices, , drop = FALSE]
    metadata <- unique(z[metadata_keys])
    mode <- mode_region(metadata$Region)
    m <- z[which(z$is_mollusca == "1" & z$is_excluding_unlithified_pass == "1"), , drop = FALSE]
    T <- length(unique(m$collection_no))
    frequencies <- sort(as.integer(table(m$genus)), decreasing = TRUE)
    S <- length(frequencies)
    stopifnot(sum(frequencies) == nrow(m), all(frequencies <= T),
              !anyDuplicated(m[c("collection_no", "genus")]))
    refs <- unique(m$reference_no[!is.na(m$reference_no)])
    n_refs <- if (length(refs)) length(refs) else NA_integer_
    multiton <- if (S) sum(frequencies > 1) / S else NA_real_
    row_gate <- nrow(m) > 10L
    quality <- nrow(metadata) >= 10L & n_refs >= 2L & multiton >= 0.3
    estimated <- estimate(T, frequencies, row_gate)
    eligible <- isTRUE(row_gate & quality & estimated$estimator_status == "finite_within_cap")
    cell <- data.frame(
      subset = subset, stage = z$stage[[1]], cell_id = z$cell_id[[1]],
      cell_paleolat = z$cell_paleolat[[1]], cell_paleolng = z$cell_paleolng[[1]],
      band = band(z$cell_paleolat[[1]]), region = mode[["region"]],
      region_status = mode[["status"]], n_pool_rows = nrow(z),
      clade_agnostic_n_total_colls = nrow(metadata),
      clade_agnostic_distinct_collection_ids = length(unique(z$collection_no)),
      n_mollusca_rows = nrow(m), n_colls = T, n_genera = S, n_refs = n_refs,
      singletons = sum(frequencies == 1L), doubletons = sum(frequencies == 2L),
      multiton_ratio = multiton, row_gate = row_gate,
      collection_quality = nrow(metadata) >= 10L, reference_quality = n_refs >= 2L,
      multiton_quality = multiton >= 0.3, quality = quality,
      eligible = eligible, frequencies = paste(frequencies, collapse = ","),
      stringsAsFactors = FALSE
    )
    all_cells[[length(all_cells) + 1L]] <- cbind(cell, as.data.frame(estimated))
  }
  message(subset, ": ", nrow(x), " prepared rows; ", length(groups), " stage-cells")
}
cells <- do.call(rbind, all_cells)
cells <- cells[order(cells$subset, cells$stage, cells$cell_id), ]
write_tsv(cells, "cells.tsv")
regions <- sort(unique(c(cells$region, "AF", "AOC", "AS", "ATA", "AUS", "CAm",
                         "EU", "IOC", "NAm", "POC", "RoW", "SA", "UNKNOWN")))
support <- expand.grid(subset = c("original", "dated_public_member"),
                       stage = c("Albian", "Campanian"), region = regions,
                       band = c("tropical", "midlatitude", "higher"),
                       stringsAsFactors = FALSE)
counts <- lapply(seq_len(nrow(support)), function(i) {
  key <- support[i, ]
  y <- cells[cells$subset == key$subset & cells$stage == key$stage &
               cells$region == key$region & cells$band == key$band, ]
  data.frame(cells_with_pool = nrow(y), cells_with_mollusca = sum(y$n_mollusca_rows > 0),
             cells_gt10_mollusca = sum(y$row_gate),
             cells_after_quality = sum(y$row_gate & y$quality, na.rm = TRUE),
             cells_eligible = sum(y$eligible),
             quality_passing_estimator_error = sum(y$row_gate & y$quality &
                                                   y$estimator_status == "error", na.rm = TRUE),
             quality_passing_above_2T = sum(y$row_gate & y$quality &
                                           y$estimator_status == "above_2T", na.rm = TRUE))
})
support <- cbind(support, do.call(rbind, counts))
write_tsv(support, "regional-support.tsv")
overlap <- expand.grid(subset = c("original", "dated_public_member"),
                       region = regions, stringsAsFactors = FALSE)
for (stage in c("Albian", "Campanian")) {
  for (b in c("tropical", "midlatitude")) {
    name <- paste(stage, b, sep = "_")
    overlap[[name]] <- vapply(seq_len(nrow(overlap)), function(i) {
      y <- support[support$subset == overlap$subset[[i]] &
                     support$region == overlap$region[[i]] &
                     support$stage == stage & support$band == b, ]
      stopifnot(nrow(y) == 1L)
      y$cells_eligible
    }, integer(1))
  }
}
overlap$both_bands_both_stages <- apply(overlap[, 3:6] > 0, 1, all)
overlap$outside_eu_nam_known <- !overlap$region %in% c("EU", "NAm", "UNKNOWN")
write_tsv(overlap, "region-overlap.tsv")
timing <- as.data.frame(as.list(unclass(proc.time() - started)))
write_tsv(timing, "timing.tsv")
message("Complete: ", nrow(cells), " stage-cell results; ", sum(cells$eligible), " eligible")

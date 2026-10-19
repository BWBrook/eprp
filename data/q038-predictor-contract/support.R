# Q-038 prospective predictor contract: support table for Rhynchonellata and Bivalvia.
# Reads the Monarrez, Heim & Payne 2023 deposit (Dryad 10.5061/dryad.931zcrjqw, CC0) as data only. Base R.
# Run from the repository root:  Rscript --vanilla data/q038-predictor-contract/support.R
# Outputs (tracked): stages.tsv, mapping_check.tsv, events.tsv, background.tsv, units.tsv
raw <- "data/raw/monarrez2023"
out <- "data/q038-predictor-contract"
classes <- c("Rhynchonellata", "Bivalvia")
events <- c(LOME = 7, LD = 21, EP = 38, ETr = 45, KPg = 68)  # interval k -> k+1 ending at each boundary

occ <- read.csv(file.path(raw, "pbdb.cleaned.classes.csv"))
o <- occ[occ$class %in% classes, ]
stopifnot(all(is.na(o$late_interval) | o$late_interval == "" | o$late_interval == o$early_interval))
bases <- sort(unique(o$max_ma), decreasing = TRUE)
o$s <- match(o$max_ma, bases)  # stage index, 1 = oldest
stages <- unique(o[, c("s", "early_interval", "max_ma", "min_ma")])
stages <- stages[order(stages$s), ]
stopifnot(!anyDuplicated(stages$s))
write.table(stages, file.path(out, "stages.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
S <- nrow(stages)

# Units. Primary: genus, keyed by PBDB genus_no (subgenera merged into their genus).
# Sensitivity: the authors' convention, the name as deposited (a subgenus is its own unit).
o$unit_genus <- paste0("g", o$genus_no)
o$unit_author <- o$genus

# Mapping check against the deposited capture histories (authors' unit, names unique in both).
e <- new.env(); load(file.path(raw, "encounter_history_bs_gr_5class_Big5.Rdata"), envir = e); eh <- get(ls(e)[1], envir = e)
eh <- eh[eh$class %in% classes & !(eh$genus %in% eh$genus[duplicated(eh$genus)]), ]
bits <- do.call(rbind, lapply(strsplit(as.character(eh$ch), ""), as.integer))
pres_author <- tapply(o$s, o$unit_author, function(v) sort(unique(v)))
chk <- sapply(seq_len(nrow(eh)), function(i) {
  p <- pres_author[[eh$genus[i]]]
  if (is.null(p)) return(NA)
  identical(as.integer(p[p <= ncol(bits)]), which(bits[i, ] == 1))
})
mapping <- data.frame(genera_checked = sum(!is.na(chk)), identical = sum(chk, na.rm = TRUE),
                      not_in_occurrences = sum(is.na(chk)), occasions = ncol(bits), stages_with_occurrences = S)
write.table(mapping, file.path(out, "mapping_check.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(mapping)

gc_max <- function(lat, lng) {  # maximum great-circle distance (km) among distinct located points
  p <- unique(cbind(lat, lng))
  if (nrow(p) < 2) return(0)
  r <- pi / 180; la <- p[, 1] * r; lo <- p[, 2] * r
  m <- 0
  for (i in seq_len(nrow(p) - 1)) {
    j <- (i + 1):nrow(p)
    a <- sin((la[j] - la[i]) / 2)^2 + cos(la[i]) * cos(la[j]) * sin((lo[j] - lo[i]) / 2)^2
    m <- max(m, 2 * 6371 * asin(pmin(1, sqrt(a))))
  }
  m
}

unit_table <- function(key) {
  u <- split(o, list(o[[key]]), drop = TRUE)
  do.call(rbind, lapply(names(u), function(nm) {
    x <- u[[nm]]
    data.frame(unit = nm, class = x$class[1], fad = min(x$s), lad = max(x$s),
               logvol = if (all(is.na(x$logvol))) NA else x$logvol[!is.na(x$logvol)][1],
               order_known = any(!is.na(x$order) & x$order != ""), family_known = any(!is.na(x$family) & x$family != ""))
  }))
}

stage_predictors <- function(key, k) {  # predictors from stage k only, per unit with a record at k
  x <- o[o$s == k, ]
  if (!nrow(x)) return(data.frame(unit = character()))
  u <- split(x, x[[key]], drop = TRUE)
  do.call(rbind, lapply(names(u), function(nm) {
    y <- u[[nm]]; loc <- !is.na(y$paleolat) & !is.na(y$paleolng)
    data.frame(unit = nm, n_occ = nrow(y), n_loc = sum(loc), n_coll = length(unique(y$collection_no)),
               n_ref = length(unique(y$reference_no)),
               range_km = if (any(loc)) gc_max(y$paleolat[loc], y$paleolng[loc]) else NA)
  }))
}

summarise_unit <- function(key) {
  U <- unit_table(key)
  rows <- list()
  for (cl in classes) {
    Uc <- U[U$class == cl, ]
    for (k in 2:(S - 1)) {
      coh <- Uc[Uc$fad <= k & Uc$lad >= k, ]
      if (!nrow(coh)) next
      lost <- coh$lad == k
      pr <- stage_predictors(key, k - 1)
      pr <- pr[match(coh$unit, pr$unit), ]
      new <- coh$fad == k
      rec_prev <- !new & !is.na(pr$n_occ)
      rows[[length(rows) + 1]] <- data.frame(
        class = cl, k = k, stage = stages$early_interval[k], N = nrow(coh), D = sum(lost),
        new_at_k = sum(new), D_new = sum(lost & new),
        gap_at_prev = sum(!new & !rec_prev), D_gap = sum(lost & !new & !rec_prev),
        recorded_prev = sum(rec_prev), D_recorded_prev = sum(lost & rec_prev),
        range_defined_prev = sum(rec_prev & !is.na(pr$range_km)),
        single_locality_prev = sum(rec_prev & !is.na(pr$range_km) & pr$range_km == 0),
        median_refs_prev = if (any(rec_prev)) median(pr$n_ref[rec_prev]) else NA,
        one_ref_prev = sum(rec_prev & pr$n_ref == 1),
        size_known = sum(!is.na(coh$logvol)), family_known = sum(coh$family_known))
    }
  }
  list(units = U, intervals = do.call(rbind, rows))
}

g <- summarise_unit("unit_genus")
a <- summarise_unit("unit_author")
ev <- function(t, lab) {
  x <- t[t$k %in% events, ]
  x$event <- names(events)[match(x$k, events)]
  x$unit <- lab
  x
}
evt <- rbind(ev(g$intervals, "genus_no (primary)"), ev(a$intervals, "deposited name (authors)"))
evt <- evt[, c("unit", "class", "event", "k", "stage", setdiff(names(evt), c("unit", "class", "event", "k", "stage")))]
write.table(evt, file.path(out, "events.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
bg <- g$intervals[!(g$intervals$k %in% events), ]
bgs <- do.call(rbind, lapply(split(bg, bg$class), function(x) {
  inf <- x$D > 0 & x$D < x$N
  data.frame(class = x$class[1], intervals = nrow(x), informative = sum(inf), median_N = median(x$N), median_D = median(x$D),
             median_loss_fraction = median(x$D / x$N), share_new = sum(x$new_at_k) / sum(x$N), share_gap = sum(x$gap_at_prev) / sum(x$N),
             share_recorded_prev = sum(x$recorded_prev) / sum(x$N), share_range_defined_of_recorded = sum(x$range_defined_prev) / sum(x$recorded_prev),
             share_single_locality_of_defined = sum(x$single_locality_prev) / sum(x$range_defined_prev),
             share_one_reference_of_recorded = sum(x$one_ref_prev) / sum(x$recorded_prev),
             share_losses_new = sum(x$D_new) / sum(x$D), share_losses_gap = sum(x$D_gap) / sum(x$D))
}))
write.table(bgs, file.path(out, "background.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
un <- do.call(rbind, lapply(list(list(g$units, "genus_no (primary)"), list(a$units, "deposited name (authors)")), function(z) {
  do.call(rbind, lapply(split(z[[1]], z[[1]]$class), function(x)
    data.frame(unit = z[[2]], class = x$class[1], units = nrow(x), size_known = mean(!is.na(x$logvol)),
               order_known = mean(x$order_known), family_known = mean(x$family_known))))
}))
write.table(un, file.path(out, "units.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(stages[stages$s %in% c(events, events + 1), ], row.names = FALSE)
print(evt[, 1:12], row.names = FALSE)
print(bgs, row.names = FALSE)
print(un, row.names = FALSE)

# Recency: for each incoming genus (first record before stage k), stages between its last record before k and k - 1.
# Under the primary rule its predictors come from that most recent recorded stage, so every incoming genus has one.
pres_g <- tapply(o$s, o$unit_genus, function(v) sort(unique(v)))
U <- g$units
rec <- list()
for (cl in classes) {
  Uc <- U[U$class == cl, ]
  for (k in 2:(S - 1)) {
    inc <- Uc[Uc$fad <= k - 1 & Uc$lad >= k, ]
    if (!nrow(inc)) next
    r <- sapply(inc$unit, function(u) { p <- pres_g[[u]]; k - 1 - max(p[p <= k - 1]) })
    lost <- inc$lad == k
    rec[[length(rec) + 1]] <- data.frame(class = cl, k = k, event = if (k %in% events) names(events)[events == k] else "background",
                                         N_incoming = nrow(inc), D_incoming = sum(lost),
                                         r0 = sum(r == 0), r1 = sum(r == 1), r2 = sum(r == 2), r3plus = sum(r >= 3),
                                         D_r0 = sum(lost & r == 0), D_r1plus = sum(lost & r >= 1))
  }
}
rec <- do.call(rbind, rec)
recs <- rbind(rec[rec$event != "background", ],
              do.call(rbind, lapply(split(rec[rec$event == "background", ], rec$class[rec$event == "background"]), function(x)
                data.frame(class = x$class[1], k = NA, event = "background (sum)", N_incoming = sum(x$N_incoming), D_incoming = sum(x$D_incoming),
                           r0 = sum(x$r0), r1 = sum(x$r1), r2 = sum(x$r2), r3plus = sum(x$r3plus), D_r0 = sum(x$D_r0), D_r1plus = sum(x$D_r1plus)))))
write.table(recs, file.path(out, "recency.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(recs, row.names = FALSE)
sing <- do.call(rbind, lapply(classes, function(cl) {
  x <- g$intervals[g$intervals$class == cl & !(g$intervals$k %in% events), ]
  Uc <- U[U$class == cl, ]
  data.frame(class = cl, losses_new_at_k = sum(x$D_new), singletons = sum(Uc$fad == Uc$lad))
}))
print(sing, row.names = FALSE)

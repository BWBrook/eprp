# Q-012 Triton joint exposure audit (support only; no survival outcomes used).
# Base R. Run from the repository root, in order:
#   Rscript data/q012-exposure-support/names.R
#   uv run data/q012-exposure-support/crosswalk.py data/q012-exposure-support/triton_names.txt
#   Rscript data/q012-exposure-support/build.R
#
# Definitions (first fixed 15 October 2026; revised 16 October before rerun,
# after Codex's freeze check, 76/1686):
# - Occurrences: Triton v4 2023 update, triton.pres, trim == "inc", non-missing
#   pal.lat, mapped to Lamyman S1 morphospecies through name_crosswalk.tsv
#   (exact, Tree1 "Name Changed", backticks; nothing else), and kept only
#   within the species' S1 range.
# - Cells: 1-Myr age bins (floor(age)) x 10-degree signed palaeolatitude bands.
# - Lineage occurrences: the union of member morphospecies' kept occurrences
#   within the lineage's own range.
# - Lineage coverage: share of the lineage's 1-Myr bins with >= 1 occurrence;
#   "covered" if >= 0.5.
# - Exposure covariate E (the model input): per lineage and 1-Myr bin, the mean
#   |palaeolatitude| of the lineage's occurrences (all members). The value used
#   for the hazard in bin b is PAST-ONLY: the observed value from the nearest
#   OLDER bin with data, at most 2 bins older; the bin's own (contemporaneous)
#   mean is never used, so no information from later in the bin or from later
#   bins enters. Otherwise missing (indicator). Standardised across observed
#   lineage-bins.
# - Pair comparisons over bins where both lineages exist and both have data:
#   (a) Jaccard similarity of occupied (bin, band) cells, members shared by the
#       pair excluded from both sides: < 3 joint data bins "insufficient";
#       J < 0.5 "different"; else "similar";
#   (b) mean absolute difference in the lineages' bin means of |palaeolatitude|
#       (the E scale, all members): "E-different" if >= 5 degrees with >= 3
#       joint data bins.
#   (c) added after the first rerun, because (b) is inflated by sampling noise
#       in sparse bins and is reported unchanged beside it: the absolute
#       difference between the two lineages' means over the same joint bins,
#       "E-systematic-different" if >= 5 degrees with >= 3 joint data bins.

out_dir <- "data/q012-exposure-support"
ev_dir <- "data/q012-event-dictionary"
rdata <- "data/raw/triton/triton_update_2023.RData"

cat("triton RData md5", tools::md5sum(rdata), "\n")
e <- new.env()
load(rdata, envir = e)
all_triton <- get("triton.pres", e)
tp <- all_triton[all_triton$trim == "inc" & !is.na(all_triton$pal.lat) & !is.na(all_triton$age),
                 c("species", "age", "pal.lat", "holeID")]
strip <- function(s) gsub("^[[:space:] ]+|[[:space:] ]+$", "", s)
tp$species <- strip(tp$species)

xw <- read.delim(file.path(out_dir, "name_crosswalk.tsv"), stringsAsFactors = FALSE)
xw <- xw[xw$s1_name != "", ]
tp$s1 <- xw$s1_name[match(tp$species, xw$triton_name)]
tp <- tp[!is.na(tp$s1), ]

sp <- read.delim(file.path(ev_dir, "species.tsv"), stringsAsFactors = FALSE)
sp <- sp[sp$in_scope == "True", ]
sp$morphospecies <- strip(sp$morphospecies)
le <- read.delim(file.path(ev_dir, "lineage_edges.tsv"), stringsAsFactors = FALSE)
le <- le[le$in_scope == "True", ]

rng <- setNames(lapply(seq_len(nrow(sp)), function(i) c(as.numeric(sp$end_Ma[i]), as.numeric(sp$start_Ma[i]))), sp$morphospecies)
tp <- tp[tp$s1 %in% names(rng), ]
inr <- mapply(function(s, a) a >= rng[[s]][1] & a <= rng[[s]][2], tp$s1, tp$age)
tp <- tp[inr, ]
tp$bin <- floor(tp$age)
tp$band <- floor(tp$pal.lat / 10)

species_tab <- data.frame(
  morphospecies = sp$morphospecies,
  crosswalk_rule = ifelse(sp$morphospecies %in% xw$s1_name, xw$rule[match(sp$morphospecies, xw$s1_name)], "none"),
  kept_occurrences = as.integer(table(factor(tp$s1, levels = sp$morphospecies))),
  stringsAsFactors = FALSE)

members <- list()
for (i in seq_len(nrow(sp))) {
  ls <- strsplit(sp$lineages[i], ";")[[1]]
  for (l in ls[ls != ""]) members[[l]] <- c(members[[l]], sp$morphospecies[i])
}
lin_range <- setNames(lapply(seq_len(nrow(le)), function(i) c(as.numeric(le$end_Ma[i]), as.numeric(le$start_Ma[i]))), le$lineage)
lin_occ <- function(l, drop = character(0)) {
  m <- setdiff(members[[l]], drop)
  r <- lin_range[[l]]
  tp[tp$s1 %in% m & tp$age >= r[1] & tp$age <= r[2], ]
}
lin_bins <- function(l) {
  r <- lin_range[[l]]
  seq(floor(r[1]), max(floor(r[1]), ceiling(r[2]) - 1))
}

cov_tab <- do.call(rbind, lapply(le$lineage, function(l) {
  x <- lin_occ(l)
  b <- lin_bins(l)
  data.frame(lineage = l, n_members = length(members[[l]]), n_occurrences = nrow(x),
             n_bins = length(b), bins_with_data = length(intersect(unique(x$bin), b)),
             coverage = round(length(intersect(unique(x$bin), b)) / length(b), 3),
             stringsAsFactors = FALSE)
}))
cov_tab$covered <- cov_tab$coverage >= 0.5

# Exposure covariate matrix: observed bin means, then the past-only value used by the model.
emat <- do.call(rbind, lapply(le$lineage, function(l) {
  x <- lin_occ(l)
  b <- sort(lin_bins(l), decreasing = TRUE)  # oldest bin first
  obs <- sapply(b, function(k) if (any(x$bin == k)) mean(abs(x$pal.lat[x$bin == k])) else NA)
  used <- rep(NA_real_, length(b)); src <- rep("missing", length(b))
  for (i in seq_along(b)) {
    older <- which(seq_along(b) < i & seq_along(b) >= i - 2 & !is.na(obs))
    if (length(older)) { j <- max(older); used[i] <- obs[j]; src[i] <- paste0("older_bin_lag", i - j) }
  }
  data.frame(lineage = l, bin = b, n_occ = sapply(b, function(k) sum(x$bin == k)),
             observed_mean_abs_pal_lat = round(obs, 3), used_value = round(used, 3), used_source = src,
             stringsAsFactors = FALSE)
}))
mu <- mean(emat$observed_mean_abs_pal_lat, na.rm = TRUE); sdv <- sd(emat$observed_mean_abs_pal_lat, na.rm = TRUE)
emat$E_standardised <- round((emat$used_value - mu) / sdv, 4)

compare <- function(a, b, type) {
  shared <- intersect(members[[a]], members[[b]])
  xa <- lin_occ(a, shared); xb <- lin_occ(b, shared)
  co <- intersect(lin_bins(a), lin_bins(b))
  jb <- intersect(co, intersect(unique(xa$bin), unique(xb$bin)))
  ca <- unique(paste(xa$bin, xa$band)[xa$bin %in% jb])
  cb <- unique(paste(xb$bin, xb$band)[xb$bin %in% jb])
  j <- if (length(union(ca, cb))) length(intersect(ca, cb)) / length(union(ca, cb)) else NA
  cls <- if (!length(co)) "no_coexistence" else if (length(jb) < 3) "insufficient" else if (j < 0.5) "different" else "similar"
  ea <- emat[emat$lineage == a & emat$bin %in% co, c("bin", "observed_mean_abs_pal_lat")]
  eb <- emat[emat$lineage == b & emat$bin %in% co, c("bin", "observed_mean_abs_pal_lat")]
  m <- merge(ea, eb, by = "bin")
  m <- m[!is.na(m[, 2]) & !is.na(m[, 3]), ]
  ed <- if (nrow(m)) mean(abs(m[, 2] - m[, 3])) else NA
  es <- if (nrow(m)) abs(mean(m[, 2]) - mean(m[, 3])) else NA
  ecls <- if (!length(co)) "no_coexistence" else if (nrow(m) < 3) "insufficient" else if (ed >= 5) "E_different" else "E_similar"
  scls <- if (!length(co)) "no_coexistence" else if (nrow(m) < 3) "insufficient" else if (es >= 5) "E_systematic_different" else "E_systematic_similar"
  data.frame(type = type, lineage_a = a, lineage_b = b, shared_members = length(shared),
             coexisting_bins = length(co), jaccard_joint_bins = length(jb), jaccard = round(j, 3),
             jaccard_class = cls, E_joint_bins = nrow(m), E_mean_abs_diff_deg = round(ed, 2), E_class = ecls,
             E_abs_mean_diff_deg = round(es, 2), E_systematic_class = scls,
             stringsAsFactors = FALSE)
}
pd <- le[le$ancestor %in% le$lineage, ]
pairs <- lapply(seq_len(nrow(pd)), function(i) compare(pd$ancestor[i], pd$lineage[i], paste0("parent_daughter_", pd$date_relation[i])))
kids <- split(pd$lineage, pd$ancestor)
for (k in kids) if (length(k) >= 2) for (i in 1:(length(k) - 1)) for (j in (i + 1):length(k)) pairs[[length(pairs) + 1]] <- compare(k[i], k[j], "sister")
pair_tab <- do.call(rbind, pairs)

bins_sites <- aggregate(holeID ~ bin, data = unique(tp[, c("bin", "holeID")]), FUN = length)
names(bins_sites)[2] <- "sites_with_matched_occurrences"

write.table(species_tab, file.path(out_dir, "species_triton.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(cov_tab, file.path(out_dir, "lineage_coverage.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(emat, file.path(out_dir, "lineage_bin_E.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(pair_tab, file.path(out_dir, "pair_exposure.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(bins_sites, file.path(out_dir, "bin_sites.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

sink(file.path(out_dir, "summary.txt"))
cat("in-scope S1 species:", nrow(sp), "| Triton species (inc):", length(unique(all_triton$species[all_triton$trim == "inc"])),
    "| S1 species reached by crosswalk:", sum(species_tab$crosswalk_rule != "none"), "\n")
print(table(species_tab$crosswalk_rule))
cat("kept occurrences:", nrow(tp), "| species with >=1 kept:", sum(species_tab$kept_occurrences > 0), "\n")
cat("lineages:", nrow(cov_tab), "| with any data:", sum(cov_tab$n_occurrences > 0), "| covered (>=0.5 of bins):", sum(cov_tab$covered), "\n")
cat("median lineage coverage:", median(cov_tab$coverage), "\n")
cat("lineage-bins:", nrow(emat), "| E used source:\n"); print(table(emat$used_source))
cat("E standardisation: mean", round(mu, 3), "sd", round(sdv, 3), "\n")
cat("Jaccard classes:\n"); print(table(pair_tab$type, pair_tab$jaccard_class))
cat("E classes (>= 5 degrees):\n"); print(table(pair_tab$type, pair_tab$E_class))
cat("E systematic classes (|difference of means| >= 5 degrees):\n"); print(table(pair_tab$type, pair_tab$E_systematic_class))
cat("pairs with shared members:", sum(pair_tab$shared_members > 0), "\n")
sink()
cat(readLines(file.path(out_dir, "summary.txt")), sep = "\n")

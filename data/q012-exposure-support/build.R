# Q-012 Triton joint exposure audit (support only; no survival outcomes used).
# Base R. Run from the repository root:  Rscript data/q012-exposure-support/build.R
#
# Definitions (fixed before the first run, 15 October 2026):
# - Occurrences: Triton v4 2023 update, triton.pres, trim == "inc", non-missing
#   pal.lat, matched to Lamyman S1 morphospecies by exact name (outer
#   whitespace stripped), and kept only within the species' S1 range.
# - Cells: 1-Myr age bins (floor(age)) x 10-degree signed palaeolatitude bands.
# - Lineage occurrences: the union of member morphospecies' kept occurrences
#   falling within the lineage's own range. Membership is many-to-many, so for
#   each relative pair any member shared by both lineages is excluded from both.
# - Lineage coverage: share of the lineage's 1-Myr bins with >= 1 occurrence;
#   "covered" if >= 0.5.
# - Pair comparison: over bins where both lineages exist and both have data,
#   Jaccard similarity of occupied (bin, band) cells. Classes: no co-existence;
#   insufficient (< 3 joint data bins); different (J < 0.5); similar (J >= 0.5).

out_dir <- "data/q012-exposure-support"
ev_dir <- "data/q012-event-dictionary"
rdata <- "data/raw/triton/triton_update_2023.RData"

cat("triton RData md5", tools::md5sum(rdata), "\n")
e <- new.env()
load(rdata, envir = e)
tp <- get("triton.pres", e)
tp <- tp[tp$trim == "inc" & !is.na(tp$pal.lat) & !is.na(tp$age), c("species", "age", "pal.lat", "holeID")]
strip <- function(s) gsub("^[[:space:] ]+|[[:space:] ]+$", "", s)
tp$species <- strip(tp$species)

sp <- read.delim(file.path(ev_dir, "species.tsv"), stringsAsFactors = FALSE)
sp <- sp[sp$in_scope == "True", ]
sp$morphospecies <- strip(sp$morphospecies)
le <- read.delim(file.path(ev_dir, "lineage_edges.tsv"), stringsAsFactors = FALSE)
le <- le[le$in_scope == "True", ]

matched <- intersect(unique(tp$species), sp$morphospecies)
tp <- tp[tp$species %in% matched, ]
rng <- setNames(lapply(seq_len(nrow(sp)), function(i) c(as.numeric(sp$end_Ma[i]), as.numeric(sp$start_Ma[i]))), sp$morphospecies)
inr <- mapply(function(s, a) a >= rng[[s]][1] & a <= rng[[s]][2], tp$species, tp$age)
tp <- tp[inr, ]
tp$bin <- floor(tp$age)
tp$band <- floor(tp$pal.lat / 10)

species_tab <- data.frame(
  morphospecies = sp$morphospecies,
  in_triton = sp$morphospecies %in% unique(get("triton.pres", e)$species),
  kept_occurrences = as.integer(table(factor(tp$species, levels = sp$morphospecies))),
  stringsAsFactors = FALSE)

members <- setNames(lapply(seq_len(nrow(sp)), function(i) character(0)), character(0))
for (i in seq_len(nrow(sp))) {
  ls <- strsplit(sp$lineages[i], ";")[[1]]
  for (l in ls[ls != ""]) members[[l]] <- c(members[[l]], sp$morphospecies[i])
}
lin_range <- setNames(lapply(seq_len(nrow(le)), function(i) c(as.numeric(le$end_Ma[i]), as.numeric(le$start_Ma[i]))), le$lineage)

lin_occ <- function(l, drop = character(0)) {
  m <- setdiff(members[[l]], drop)
  r <- lin_range[[l]]
  x <- tp[tp$species %in% m & tp$age >= r[1] & tp$age <= r[2], ]
  x
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
             mean_abs_pal_lat = if (nrow(x)) round(mean(abs(x$pal.lat)), 2) else NA,
             stringsAsFactors = FALSE)
}))
cov_tab$covered <- cov_tab$coverage >= 0.5

compare <- function(a, b, type) {
  shared <- intersect(members[[a]], members[[b]])
  xa <- lin_occ(a, shared); xb <- lin_occ(b, shared)
  co <- intersect(lin_bins(a), lin_bins(b))
  jb <- intersect(co, intersect(unique(xa$bin), unique(xb$bin)))
  ca <- unique(paste(xa$bin, xa$band)[xa$bin %in% jb])
  cb <- unique(paste(xb$bin, xb$band)[xb$bin %in% jb])
  j <- if (length(union(ca, cb))) length(intersect(ca, cb)) / length(union(ca, cb)) else NA
  cls <- if (!length(co)) "no_coexistence" else if (length(jb) < 3) "insufficient" else if (j < 0.5) "different" else "similar"
  data.frame(type = type, lineage_a = a, lineage_b = b, shared_members_excluded = length(shared),
             coexisting_bins = length(co), joint_data_bins = length(jb), jaccard = round(j, 3),
             abs_pal_lat_diff = if (nrow(xa[xa$bin %in% jb, ]) && nrow(xb[xb$bin %in% jb, ]))
               round(abs(mean(abs(xa$pal.lat[xa$bin %in% jb])) - mean(abs(xb$pal.lat[xb$bin %in% jb]))), 2) else NA,
             class = cls, stringsAsFactors = FALSE)
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
write.table(pair_tab, file.path(out_dir, "pair_exposure.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(bins_sites, file.path(out_dir, "bin_sites.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

sink(file.path(out_dir, "summary.txt"))
cat("in-scope S1 species:", nrow(sp), "| Triton species:", length(unique(get("triton.pres", e)$species)),
    "| exact-name matches:", length(matched), "\n")
cat("kept occurrences (inc, pal.lat, within S1 range):", nrow(tp), "| species with >=1 kept:", sum(species_tab$kept_occurrences > 0), "\n")
cat("lineages:", nrow(cov_tab), "| with any data:", sum(cov_tab$n_occurrences > 0), "| covered (>=0.5 of bins):", sum(cov_tab$covered), "\n")
cat("median lineage coverage:", median(cov_tab$coverage), "\n")
print(table(pair_tab$type, pair_tab$class))
cat("pairs with shared members excluded:", sum(pair_tab$shared_members_excluded > 0), "\n")
sink()
cat(readLines(file.path(out_dir, "summary.txt")), sep = "\n")

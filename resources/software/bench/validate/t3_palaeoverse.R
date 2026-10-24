# Tranche-3 tests V1-V5 (palaeoverse) and F1-F2 (fossilbrush) (../VALIDATION_T3.md).
# Usage: Rscript t3_palaeoverse.R <outdir> <ics2024_table> <isc_versions_table> [reps]
suppressPackageStartupMessages({library(palaeoverse); library(fossilbrush); library(jsonlite)})
args <- commandArgs(TRUE)
outdir <- args[1]; ics_file <- args[2]; isc_file <- args[3]; reps <- if (length(args) > 3) as.integer(args[4]) else 200
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
res <- list(meta = list(date = format(Sys.time(), tz = "UTC"), reps = reps,
                        packages = as.list(sapply(c("palaeoverse", "fossilbrush"), function(p) as.character(packageVersion(p))))))

# synthetic occurrences (A1): 500 taxa with ranges of mean 20 Myr; each occurrence's
# age range (mean width 5 Myr) is centred on a time inside its taxon's range
set.seed(301)
n <- 20000
orig <- runif(500, 20, 538.8); ext <- pmax(0.5, orig - rexp(500, 1 / 20))
tax <- sample(500, n, replace = TRUE)
centre <- runif(n, ext[tax], orig[tax]); width <- rexp(n, 1 / 5)
mx <- pmin(538.8, centre + width / 2); mn <- pmax(0, centre - width / 2)
occ <- data.frame(id = seq_len(n), genus = paste0("T", tax), max_ma = mx, min_ma = mn)
bins <- time_bins(rank = "stage", scale = "GTS2020")
overlap <- function(i) pmax(0, pmin(occ$max_ma[i], bins$max_ma) - pmax(occ$min_ma[i], bins$min_ma))
ov <- t(vapply(seq_len(n), overlap, numeric(nrow(bins))))

# V1
mid <- (occ$max_ma + occ$min_ma) / 2
truth_mid <- bins$bin[vapply(mid, function(m) which(bins$max_ma > m & bins$min_ma <= m)[1], 1L)]
truth_maj <- bins$bin[max.col(ov, ties.method = "first")]
tie <- apply(ov, 1, function(r) sum(r == max(r)) > 1)
b_mid <- bin_time(occ, bins = bins, method = "mid")
b_maj <- bin_time(occ, bins = bins, method = "majority")
res$V1 <- list(mid_agree = mean(b_mid$bin_assignment == truth_mid), maj_agree = mean(b_maj$bin_assignment[!tie] == truth_maj[!tie]),
               n_ties = sum(tie), mid_disagree = sum(b_mid$bin_assignment != truth_mid), maj_disagree = sum(b_maj$bin_assignment[!tie] != truth_maj[!tie]),
               pass = all(b_mid$bin_assignment == truth_mid) && all(b_maj$bin_assignment[!tie] == truth_maj[!tie]))

# V2, V3: pooled chi-square over occurrences overlapping 2-5 bins
k <- rowSums(ov > 0)
sel <- which(k >= 2 & k <= 5)
chisq_pool <- function(method) {
  set.seed(if (method == "random") 302 else 303)
  r <- bin_time(occ[sel, ], bins = bins, method = method, reps = reps)
  draws <- do.call(cbind, lapply(r, function(x) x$bin_assignment))
  obs <- exp <- numeric(0)
  for (j in seq_along(sel)) {
    i <- sel[j]; b <- bins$bin[ov[i, ] > 0]
    p <- if (method == "random") rep(1 / length(b), length(b)) else ov[i, ov[i, ] > 0] / sum(ov[i, ])
    o <- tabulate(match(draws[j, ], b), nbins = length(b))
    obs <- c(obs, o); exp <- c(exp, p * reps)
  }
  stat <- sum((obs - exp)^2 / exp); df <- length(obs) - length(sel)
  list(occurrences = length(sel), cells = length(obs), chisq = stat, df = df, p = pchisq(stat, df, lower.tail = FALSE))
}
res$V2 <- chisq_pool("random"); res$V2$pass <- res$V2$p > 0.001
res$V3 <- chisq_pool("point"); res$V3$pass <- res$V3$p > 0.001

# V4
tr <- tax_range_time(occ, name = "genus")
own <- aggregate(cbind(max_ma, min_ma) ~ genus, data = occ, FUN = function(v) v[1])
own$fad <- tapply(occ$max_ma, occ$genus, max)[own$genus]; own$lad <- tapply(occ$min_ma, occ$genus, min)[own$genus]
m <- match(own$genus, tr$taxon)
res$V4 <- list(taxa = nrow(own), columns = names(tr), max_fad_diff = max(abs(tr$max_ma[m] - own$fad)), max_lad_diff = max(abs(tr$min_ma[m] - own$lad)))
res$V4$pass <- res$V4$max_fad_diff < 1e-9 && res$V4$max_lad_diff < 1e-9

# V5
ics <- read.delim(ics_file)
gts <- palaeoverse::GTS2020[palaeoverse::GTS2020$rank == "stage", ]
mm <- merge(gts[, c("interval_name", "max_ma")], ics[ics$pbdb_type == "age", c("pbdb_interval", "ics_2024_12_printed")],
            by.x = "interval_name", by.y = "pbdb_interval")
mm$ics_printed_text <- mm$ics_2024_12_printed
# A1: the chart prints "174.7±0.8", "~237" and blanks; take the leading number
mm$ics_2024_12_printed <- suppressWarnings(as.numeric(sub("^~?([0-9.]+).*$", "\\1", mm$ics_2024_12_printed)))
mm$diff <- mm$max_ma - mm$ics_2024_12_printed
# A1: also chart v2020/01, the last release in the ICS RDF (palaeoverse cites chart v2020/03)
v20 <- read.delim(isc_file, check.names = FALSE)
v20 <- data.frame(interval_name = sub("^Base", "", v20$boundary_uri), ics_2020_01 = suppressWarnings(as.numeric(v20[["2020_ma"]])))
m20 <- merge(gts[, c("interval_name", "max_ma")], v20, by = "interval_name")
m20$diff <- m20$max_ma - m20$ics_2020_01
res$V5 <- list(stages_palaeoverse = nrow(gts), matched_2024 = nrow(mm), unmatched_2024 = setdiff(gts$interval_name, mm$interval_name),
               blank_2024 = mm$interval_name[is.na(mm$ics_2024_12_printed)],
               differing_2024 = mm[which(abs(mm$diff) > 0.001), c("interval_name", "max_ma", "ics_printed_text", "diff")],
               matched_2020_01 = sum(!is.na(m20$ics_2020_01)),
               differing_2020_01 = m20[which(abs(m20$diff) > 0.001), c("interval_name", "max_ma", "ics_2020_01", "diff")])

# F1: fossilbrush check_taxonomy on injected errors
set.seed(311)
syl <- c("ba", "ce", "di", "fo", "gu", "la", "me", "ni", "po", "ru", "sa", "te", "vi", "xo", "za", "ky", "phe", "tro", "mar", "len")
word <- function(nsyl) paste0(sample(syl, nsyl, TRUE), collapse = "")
cap <- function(s) paste0(toupper(substr(s, 1, 1)), substr(s, 2, nchar(s)))
uniq <- function(n, f) { out <- character(0); while (length(out) < n) out <- unique(c(out, f())); out[seq_len(n)] }
classes <- paste0(uniq(5, function() cap(word(3))), "ea")
orders <- paste0(uniq(15, function() cap(word(3))), "ida")
families <- paste0(uniq(60, function() cap(word(3))), "idae")
genera <- uniq(400, function() cap(word(4)))
ord_cls <- setNames(sample(classes, 15, TRUE), orders)
fam_ord <- setNames(sample(orders, 60, TRUE), families)
gen_fam <- setNames(sample(families, 400, TRUE), genera)
g <- sample(genera, 5000, TRUE)
tx <- data.frame(phylum = "Synthetica", class = ord_cls[fam_ord[gen_fam[g]]], order = fam_ord[gen_fam[g]], family = gen_fam[g], genus = g, row.names = NULL)
# misspellings: 30 genera, one letter substituted, in 1-3 occurrences each
miss_src <- sample(unique(tx$genus), 30); miss <- character(0)
for (s in miss_src) {
  rows <- sample(which(tx$genus == s), min(sum(tx$genus == s) - 1, sample(1:3, 1)))
  pos <- sample(2:nchar(s), 1); new <- s; substr(new, pos, pos) <- sample(setdiff(letters, substr(s, pos, pos)), 1)
  tx$genus[rows] <- new; miss <- c(miss, new)
}
# conflicts: 30 other genera get a second family in 10-30% of their rows
pool <- setdiff(unique(tx$genus), c(miss_src, miss)); pool <- pool[table(tx$genus)[pool] >= 8]
conf <- sample(pool, 30)
for (s in conf) {
  rows <- which(tx$genus == s); rows <- sample(rows, max(1, round(length(rows) * runif(1, 0.1, 0.3))))
  f2 <- sample(setdiff(families, gen_fam[s]), 1)
  tx$family[rows] <- f2; tx$order[rows] <- fam_ord[f2]; tx$class[rows] <- ord_cls[fam_ord[f2]]
}
# format errors: 10 rows of other genera get a digit or punctuation
fmt_rows <- sample(which(!tx$genus %in% c(miss, miss_src, conf)), 10)
tx$genus[fmt_rows] <- paste0(tx$genus[fmt_rows], sample(c("1", "2", "?", "."), 10, TRUE))
chk <- check_taxonomy(tx, ranks = c("phylum", "class", "order", "family", "genus"), verbose = FALSE)
syn <- chk$synonyms; syn_g <- syn[syn$level == "genus", ]
flagged_miss <- unique(c(syn_g$t1, syn_g$t2))
dup <- chk$duplicates; dup_g <- if (is.null(dup)) character(0) else dup$taxon[dup$rank == "genus"]
fmt_flag <- chk$formatting$`non-letter`$genus
res$F1 <- list(
  misspelling_recall = mean(miss %in% flagged_miss),
  misspelling_false_pairs = sum(!(syn_g$t1 %in% c(miss, miss_src) | syn_g$t2 %in% c(miss, miss_src))),
  conflict_recall = mean(conf %in% dup_g),
  conflict_false = sum(!dup_g %in% conf),
  format_recall = mean(fmt_rows %in% fmt_flag),
  format_false = sum(!fmt_flag %in% fmt_rows),
  synonym_pairs_reported = nrow(syn_g), duplicates_reported = length(dup_g))
res$F1$pass <- res$F1$misspelling_recall >= 0.9 && res$F1$conflict_recall >= 0.9 && res$F1$format_recall >= 0.9

# F2: fossilbrush flag_ranges on injected outliers
ref <- data.frame(genus = names(tapply(occ$max_ma, occ$genus, max)), fad = as.numeric(tapply(occ$max_ma, occ$genus, max)),
                  lad = as.numeric(tapply(occ$min_ma, occ$genus, min)))
set.seed(312)
fad_of <- ref$fad[match(occ$genus, ref$genus)]; lad_of <- ref$lad[match(occ$genus, ref$genus)]
old_i <- sample(which(fad_of <= 500), 50)                          # shifted ages stay inside 0-538.8 Ma
young_i <- sample(setdiff(which(lad_of >= 35), old_i), 50)
inj_old <- occ[old_i, ]; d <- runif(50, 10, 30); f <- ref$fad[match(inj_old$genus, ref$genus)]
inj_old$max_ma <- f + d; inj_old$min_ma <- f + d - 0.5
inj_young <- occ[young_i, ]; d <- runif(50, 10, 30); l <- ref$lad[match(inj_young$genus, ref$genus)]
inj_young$min_ma <- pmax(0, l - d); inj_young$max_ma <- inj_young$min_ma + 0.5
x2 <- rbind(occ, inj_old, inj_young); x2$injected <- c(rep(0, n), rep(1, 100))
fr <- flag_ranges(x = x2[, c("genus", "max_ma", "min_ma")], y = ref, xcols = c("genus", "max_ma", "min_ma"),
                  ycols = c("genus", "fad", "lad"), flag.diff = 5, verbose = FALSE)
errs <- fr[[2]]
flag_any <- apply(errs[, grepl("5", names(errs)), drop = FALSE] == 1, 1, any)
res$F2 <- list(columns = names(errs), recall = mean(flag_any[x2$injected == 1]), false_flags = sum(flag_any[x2$injected == 0]),
               recall_old = mean(flag_any[x2$injected == 1][1:50]), recall_young = mean(flag_any[x2$injected == 1][51:100]),
               injected_young_lad_below_zero_clipped = sum(inj_young$min_ma == 0))
write.table(cbind(x2, errs), file.path(outdir, "t3_flag_ranges.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
res$F2$pass <- res$F2$recall == 1 && res$F2$false_flags == 0

res$pass <- all(c(res$V1$pass, res$V2$pass, res$V3$pass, res$V4$pass, res$F1$pass, res$F2$pass))
write_json(res, file.path(outdir, "t3_palaeoverse.json"), auto_unbox = TRUE, digits = 8, pretty = TRUE)
cat(toJSON(res[setdiff(names(res), "meta")], auto_unbox = TRUE, digits = 5, pretty = TRUE), "\n")

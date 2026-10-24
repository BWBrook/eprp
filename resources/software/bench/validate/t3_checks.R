# Tranche-3 follow-up checks after the independent review (../VALIDATION_T3.md A2).
# Usage: Rscript t3_checks.R <outdir>
# 1. F1 reproduced (seed 311): every synonym pair fossilbrush reports, classified, and the
#    Jaro-Winkler distances of the missed misspellings.
# 2. bin_time on boundary and tie cases.
suppressPackageStartupMessages({library(palaeoverse); library(fossilbrush); library(stringdist); library(jsonlite)})
outdir <- commandArgs(TRUE)[1]
res <- list()

# 1. F1, the same construction as t3_palaeoverse.R
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
miss_src <- sample(unique(tx$genus), 30); miss <- character(0)
for (s in miss_src) {
  rows <- sample(which(tx$genus == s), min(sum(tx$genus == s) - 1, sample(1:3, 1)))
  pos <- sample(2:nchar(s), 1); new <- s; substr(new, pos, pos) <- sample(setdiff(letters, substr(s, pos, pos)), 1)
  tx$genus[rows] <- new; miss <- c(miss, new)
}
pool <- setdiff(unique(tx$genus), c(miss_src, miss)); pool <- pool[table(tx$genus)[pool] >= 8]
conf <- sample(pool, 30)
for (s in conf) {
  rows <- which(tx$genus == s); rows <- sample(rows, max(1, round(length(rows) * runif(1, 0.1, 0.3))))
  f2 <- sample(setdiff(families, gen_fam[s]), 1)
  tx$family[rows] <- f2; tx$order[rows] <- fam_ord[f2]; tx$class[rows] <- ord_cls[fam_ord[f2]]
}
fmt_rows <- sample(which(!tx$genus %in% c(miss, miss_src, conf)), 10)
fmt_names <- paste0(tx$genus[fmt_rows], sample(c("1", "2", "?", "."), 10, TRUE))
tx$genus[fmt_rows] <- fmt_names
chk <- check_taxonomy(tx, ranks = c("phylum", "class", "order", "family", "genus"), verbose = FALSE)
syn <- chk$synonyms[chk$synonyms$level == "genus", ]
syn$kind <- ifelse(syn$t1 %in% miss | syn$t2 %in% miss, "injected misspelling",
              ifelse(syn$t1 %in% fmt_names | syn$t2 %in% fmt_names, "injected format error", "clean names"))
missed <- miss[!miss %in% c(syn$t1, syn$t2)]
src_of <- setNames(miss_src, miss)
res$F1_pairs <- list(by_kind = as.list(table(syn$kind)), clean_pairs = syn[syn$kind == "clean names", c("t1", "t2")],
                     missed = data.frame(misspelling = missed, source = unname(src_of[missed]),
                                         jw_distance = stringdist(missed, src_of[missed], method = "jw", p = 0),
                                         same_family = gen_fam[src_of[missed]] == tx$family[match(missed, tx$genus)]))

# 2. bin_time edge cases
bins <- time_bins(rank = "stage", scale = "GTS2020")
b <- bins[bins$max_ma > 470 & bins$min_ma < 486, c("bin", "interval_name", "max_ma", "min_ma")]
edge <- function(method, df) tryCatch({ r <- suppressWarnings(bin_time(df, bins = bins, method = method, reps = 5))
  if (is.data.frame(r)) r$bin_assignment else r[[1]]$bin_assignment }, error = function(e) paste("error:", conditionMessage(e)))
cases <- list(midpoint_on_boundary = data.frame(max_ma = 485.4, min_ma = 470.0),
              zero_width_on_boundary = data.frame(max_ma = 477.7, min_ma = 477.7),
              equal_overlap_tie = data.frame(max_ma = 479.7, min_ma = 475.7))   # 2 Myr either side of the 477.7 boundary
res$bin_edges <- list(bins = b, results = lapply(cases, function(df) sapply(c("mid", "majority", "random", "point"), edge, df = df)))
write_json(res, file.path(outdir, "t3_checks_r.json"), auto_unbox = TRUE, digits = 6, pretty = TRUE)
cat(toJSON(res, auto_unbox = TRUE, digits = 4, pretty = TRUE), "\n")

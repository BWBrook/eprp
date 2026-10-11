# Q-038 data contract: read-only inspection of the Monarrez, Heim & Payne 2023 Dryad deposit
# (10.5061/dryad.931zcrjqw, CC0). Base R only; nothing in the deposit is executed.
# Run from the repository root:  Rscript --vanilla data/q038-monarrez-contract/inspect.R
raw <- "data/raw/monarrez2023"
out <- "data/q038-monarrez-contract"

e <- new.env()
objs <- load(file.path(raw, "encounter_history_bs_gr_5class_Big5.Rdata"), envir = e)
cat("objects:", objs, "\n")
eh <- get(objs[1], envir = e)
cat("class:", class(eh), " dim:", dim(eh), "\n")
cat("first columns:", head(names(eh), 6), "\n")
cat("row names look like genera:", head(rownames(eh), 4), "\n")

ch <- as.character(eh$ch)
cat("ch storage:", typeof(eh$ch), " nchar range:", range(nchar(ch)), "\n")
cat("ch only 0/1:", all(grepl("^[01]+$", ch)), "\n")
n_occ <- nchar(ch[1])

me <- as.matrix(eh[, grep("^mass\\.ext", names(eh))])
flag_pos <- which(colSums(me) > 0)
cat("mass.ext columns:", ncol(me), " flagged positions:", flag_pos,
    " constant across genera:", all(apply(me, 2, function(v) length(unique(v)) == 1)), "\n")

bits <- do.call(rbind, lapply(strsplit(ch, ""), as.integer))
last_occ <- apply(bits, 1, function(r) max(which(r == 1)))
first_occ <- apply(bits, 1, function(r) min(which(r == 1)))
lo_tab <- tabulate(last_occ, nbins = n_occ)
# alignment: last occurrences in occasion k mean extinction in interval k -> k+1;
# compare last-occurrence counts at each flagged interval index k and at k - 1 and k + 1
align <- data.frame(flag_interval = flag_pos,
                    lo_at_k_minus_1 = lo_tab[flag_pos - 1],
                    lo_at_k = lo_tab[flag_pos],
                    lo_at_k_plus_1 = lo_tab[pmin(flag_pos + 1, n_occ)])
print(align, row.names = FALSE)
top <- order(lo_tab, decreasing = TRUE)[1:8]
cat("occasions with most last occurrences:", top, "\n  counts:", lo_tab[top], "\n")

classes <- table(eh$class)
print(classes)
span <- tapply(seq_len(nrow(eh)), eh$class, function(i) c(min(first_occ[i]), max(last_occ[i])))
print(do.call(rbind, span))

rng <- as.matrix(eh[, grep("^range", names(eh))])
cat("range columns:", ncol(rng), " NA share:", round(mean(is.na(rng)), 3), "\n")

gen <- read.csv(file.path(raw, "genus.sizes.ranges.cleaned.classes.csv"))
cat("genus table rows:", nrow(gen), " columns:", names(gen), "\n")
cat("order missing share:", round(mean(is.na(gen$order) | gen$order == ""), 3),
    " family missing share:", round(mean(is.na(gen$family) | gen$family == ""), 3), "\n")
subg <- grepl("\\(", gen$genus)
cat("subgenus-style names in genus table:", sum(subg), "of", nrow(gen), "\n")
base_names <- sub(" \\(.*$", "", gen$genus[subg])
cat("subgenus rows whose base genus also has a row:", sum(base_names %in% gen$genus), "\n")

occ <- read.csv(file.path(raw, "pbdb.cleaned.classes.csv"))
cat("occurrence rows:", nrow(occ), " columns:", ncol(occ), "\n")
cat("has paleolat/paleolng:", all(c("paleolat", "paleolng") %in% names(occ)),
    " paleolat NA share:", round(mean(is.na(occ$paleolat)), 3), "\n")
cat("paleomodel values:", paste(head(names(sort(table(occ$paleomodel), decreasing = TRUE)), 3), collapse = ", "), "\n")
one_interval <- occ$late_interval == "" | is.na(occ$late_interval) | occ$late_interval == occ$early_interval
cat("occurrences with a single named interval:", round(mean(one_interval), 3), "\n")

summary <- data.frame(
  item = c("genera", "occasions", "intervals_flagged", "ch_intact_in_rdata", "range_columns",
           "occurrences", "paleocoords_present", "order_missing_share", "subgenus_rows"),
  value = c(nrow(eh), n_occ, paste(flag_pos, collapse = ";"), all(grepl("^[01]+$", ch)) && length(unique(nchar(ch))) == 1,
            ncol(rng), nrow(occ), all(c("paleolat", "paleolng") %in% names(occ)),
            round(mean(is.na(gen$order) | gen$order == ""), 3), sum(subg)))
write.table(summary, file.path(out, "summary.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(align, file.path(out, "flag_alignment.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

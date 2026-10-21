# Q-038 attribute-ambiguity export and frozen clade policy for Rhynchonellata and Bivalvia (Codex 76/2112 item 4).
# Reads the Monarrez, Heim & Payne 2023 deposit (Dryad 10.5061/dryad.931zcrjqw, CC0) as data only. Base R.
# Run from the repository root:  Rscript --vanilla data/q038-predictor-contract/ambiguity.R
# Outputs (tracked): ambiguity.tsv (one row per genus_no with more than one name, size, order or family),
#                    ambiguity_summary.tsv, name_homonyms.tsv
raw <- "data/raw/monarrez2023"
out <- "data/q038-predictor-contract"
classes <- c("Rhynchonellata", "Bivalvia")

occ <- read.csv(file.path(raw, "pbdb.cleaned.classes.csv"))
o <- occ[occ$class %in% classes, ]
fmt <- function(tab) if (length(tab)) paste0(names(tab), ":", tab, collapse = "|") else ""

# Frozen clade policy, fixed here before any fit or score. Family: the label carried by the most distinct references
# among the genus's occurrences; a tie at the top is the explicit level "unresolved"; no label is "unknown". Order is
# resolved per family, not per genus: most order conflicts are nomenclatural (for example Veneroida against Cardiida
# or Lucinida for one family, entered under subgenus names), so each family takes the order carried by the most
# distinct references across all its genera. A genus without a resolved family keeps its own modal order.
modal <- function(labels, refs) {
  keep <- !is.na(labels) & labels != ""
  if (!any(keep)) return("unknown")
  n <- tapply(refs[keep], labels[keep], function(r) length(unique(r)))
  top <- names(n)[n == max(n)]
  if (length(top) > 1) "unresolved" else top
}

rows <- lapply(split(o, o$genus_no), function(x) {
  nm <- table(x$genus)
  sz <- sort(unique(round(x$logvol[!is.na(x$logvol)], 9)))
  ordr <- tapply(x$reference_no, x$order, function(r) length(unique(r)))
  fam <- tapply(x$reference_no, x$family, function(r) length(unique(r)))
  ordr <- ordr[names(ordr) != ""]; fam <- fam[names(fam) != ""]
  data.frame(class = x$class[1], genus_no = x$genus_no[1], occurrences = nrow(x),
             duplicated_occurrence_rows = sum(duplicated(x$occurrence_no)),
             names_n = length(nm), names = fmt(nm),
             sizes_n = length(sz), logvol_min = if (length(sz)) min(sz) else NA, logvol_max = if (length(sz)) max(sz) else NA,
             orders_n = length(ordr), orders_by_refs = fmt(ordr), families_n = length(fam), families_by_refs = fmt(fam),
             order_policy = modal(x$order, x$reference_no), family_policy = modal(x$family, x$reference_no))
})
A <- do.call(rbind, rows)
o$family_policy <- A$family_policy[match(o$genus_no, A$genus_no)]
fo <- tapply(seq_len(nrow(o)), o$family_policy, function(i) modal(o$order[i], o$reference_no[i]))
A$order_policy <- ifelse(A$family_policy %in% c("unknown", "unresolved"), A$order_policy, fo[A$family_policy])
A$order_differs_from_own_modal <- A$order_policy != vapply(split(o, o$genus_no), function(x) modal(x$order, x$reference_no), "")[as.character(A$genus_no)]
amb <- A[A$names_n > 1 | A$sizes_n > 1 | A$orders_n > 1 | A$families_n > 1 | A$order_differs_from_own_modal, ]
write.table(amb[order(amb$class, amb$genus_no), ], file.path(out, "ambiguity.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

summ <- do.call(rbind, lapply(split(A, A$class), function(x)
  data.frame(class = x$class[1], genus_ids = nrow(x), multiple_names = sum(x$names_n > 1), multiple_sizes = sum(x$sizes_n > 1),
             multiple_orders = sum(x$orders_n > 1), multiple_families = sum(x$families_n > 1),
             any_ambiguity = sum(x$names_n > 1 | x$sizes_n > 1 | x$orders_n > 1 | x$families_n > 1),
             order_unresolved = sum(x$order_policy == "unresolved"), order_unknown = sum(x$order_policy == "unknown"),
             family_unresolved = sum(x$family_policy == "unresolved"), family_unknown = sum(x$family_policy == "unknown"),
             order_set_by_family_not_own_modal = sum(x$order_differs_from_own_modal),
             duplicated_occurrence_rows = sum(x$duplicated_occurrence_rows))))
write.table(summ, file.path(out, "ambiguity_summary.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(summ, row.names = FALSE)

# Deposited names that span more than one genus_no (homonyms and reassignments): name keys cannot stand in for genus IDs.
hn <- tapply(o$genus_no, o$genus, function(v) sort(unique(v)))
hn <- hn[lengths(hn) > 1]
homs <- data.frame(name = names(hn), class = o$class[match(names(hn), o$genus)],
                   genus_ids = vapply(hn, paste, "", collapse = "|"), row.names = NULL)
write.table(homs, file.path(out, "name_homonyms.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("deposited names spanning more than one genus_no:", nrow(homs), "\n")

args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 3L)
work <- normalizePath(args[1]); source <- normalizePath(args[2])
out <- normalizePath(args[3])
e <- new.env(); load(source, e)
p <- e$triton.pres
drop <- scan(file.path(work, "drop_rows.txt"), quiet = TRUE)
stopifnot(length(drop) == 16260L, !anyDuplicated(drop))
original <- readLines(file.path(work, "scripts/q012_original.R"))
stop <- which(startsWith(original, "mu <- mean"))
stopifnot(length(stop) == 1L)
original <- original[seq_len(stop - 1L)]
stopifnot(sum(grepl("round(obs, 3)", original, fixed = TRUE)) == 1L,
          sum(grepl("round(used, 3)", original, fixed = TRUE)) == 1L)
matrices <- list()
for (label in c("before", "after")) {
  env <- new.env()
  env$e <- list(triton.pres = if (label == "before") p else p[-drop, ])
  code <- character()
  for (line in original) {
    if (startsWith(line, "out_dir <-")) line <- sprintf("out_dir <- %s", encodeString(file.path(work, "inputs"), quote = '"'))
    if (startsWith(line, "ev_dir <-")) line <- sprintf("ev_dir <- %s", encodeString(file.path(work, "inputs"), quote = '"'))
    if (startsWith(line, "e <- new.env()") || startsWith(line, "load(") || startsWith(line, "cat(\"triton RData md5") || startsWith(line, "rdata <-")) next
    line <- gsub("round(obs, 3)", "obs", line, fixed = TRUE)
    line <- gsub("round(used, 3)", "used", line, fixed = TRUE)
    code <- c(code, line)
  }
  eval(parse(text = code), env)
  matrices[[label]] <- env$emat
}
a <- matrices$before; b <- matrices$after
stopifnot(identical(a$lineage, b$lineage), identical(a$bin, b$bin))
before <- a$observed_mean_abs_pal_lat; after <- b$observed_mean_abs_pal_lat
paired <- !is.na(before) & !is.na(after)
missing <- !is.na(before) & is.na(after)
stopifnot(sum(paired) == 2267L, sum(missing) == 4L,
          !any(is.na(before) & !is.na(after)))
delta <- after[paired] - before[paired]
stopifnot(sum(abs(delta) > 1e-9) == 1388L,
          sum(abs(delta) >= 1 - 1e-9) == 411L,
          abs(max(abs(delta)) - 26.89925) < 1e-9)
export <- function(mask, file) {
  table <- data.frame(lineage = a$lineage[mask], bin = a$bin[mask],
    before_mean_deg = before[mask], after_mean_deg = after[mask],
    delta_after_minus_before_deg = after[mask] - before[mask])
  table <- table[order(table$lineage, table$bin, method = "radix"), ]
  for (k in names(table)[3:5]) table[[k]] <- ifelse(is.na(table[[k]]), "NA", sprintf("%.17g", table[[k]]))
  write.table(table, file.path(out, file), sep = "\t", quote = FALSE, row.names = FALSE)
}
export(paired, "comparable.tsv")
export(missing, "newly_missing.tsv")
summary <- data.frame(field = c("R", "total_lineage_bins", "before_nonmissing", "after_nonmissing", "paired_nonmissing", "newly_missing", "both_missing", "changed_gt_1e_9", "change_ge_1_degree", "max_abs_change_deg"),
  value = c(R.version.string, nrow(a), sum(!is.na(before)), sum(!is.na(after)), sum(paired), sum(missing), sum(is.na(before) & is.na(after)), sum(abs(delta) > 1e-9), sum(abs(delta) >= 1 - 1e-9), sprintf("%.17g", max(abs(delta)))))
write.table(summary, file.path(out, "r_summary.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

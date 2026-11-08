args <- commandArgs(trailingOnly = TRUE)
work <- normalizePath(args[1]); src <- args[2]
e <- new.env(); load(src, e)
p <- e$triton.pres
drop <- scan(file.path(work, "drop_rows.txt"), quiet = TRUE)
original <- readLines(file.path(work, "scripts/q012_original.R"))
original <- original[seq_len(which(startsWith(original, "mu <- mean"))[1] - 1L)]
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
answer <- do.call(rbind, lapply(c("observed_mean_abs_pal_lat", "used_value"), function(k) {
  ok <- !is.na(a[[k]]) & !is.na(b[[k]])
  delta <- abs(a[[k]][ok] - b[[k]][ok])
  data.frame(quantity=k, paired_nonmissing=sum(ok), changed_gt_1e_9=sum(delta > 1e-9), change_ge_1_degree=sum(delta >= 1-1e-9), max_abs_change=max(delta), missingness_changed=sum(is.na(a[[k]]) != is.na(b[[k]])))
}))
options(digits = 17)
write.table(answer, file.path(work, "out/raw_mean_check.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
stopifnot(answer$changed_gt_1e_9[1] == 1388, answer$change_ge_1_degree[1] == 411)

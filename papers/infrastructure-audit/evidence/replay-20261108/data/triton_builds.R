args <- commandArgs(trailingOnly = TRUE)
work <- normalizePath(args[1]); src <- args[2]
e <- new.env(); load(src, e)
p <- e$triton.pres
drop <- scan(file.path(work, "drop_rows.txt"), quiet = TRUE)
for (label in c("before", "after")) {
  all <- p
  if (label == "after") all <- p[-drop, ]
  for (builder in c("q012", "q007")) {
    out <- file.path(work, "out", label, builder)
    dir.create(out, recursive = TRUE, showWarnings = FALSE)
    code <- readLines(file.path(work, "scripts", paste0(builder, "_original.R")))
    env <- new.env()
    env$e <- list(triton.pres = all)
    for (line in code) {
      if (startsWith(line, "out_dir <-")) line <- sprintf("out_dir <- %s", encodeString(out, quote = '"'))
      if (startsWith(line, "ev_dir <-")) line <- sprintf("ev_dir <- %s", encodeString(file.path(work, "inputs"), quote = '"'))
      if (startsWith(line, "e <- new.env()") || startsWith(line, "load(") || startsWith(line, "cat(\"triton RData md5")) next
      if (startsWith(line, "rdata <-")) next
      if (startsWith(line, "xw <- read.delim")) line <- sprintf("xw <- read.delim(%s, stringsAsFactors=FALSE)", encodeString(file.path(work, "inputs/name_crosswalk.tsv"), quote = '"'))
      if (startsWith(line, "sst <- read.csv(")) line <- sprintf("sst <- read.csv(%s)", encodeString(args[3], quote = '"'))
      env$code_lines <- c(env$code_lines, line)
    }
    eval(parse(text = env$code_lines), envir = env)
  }
}

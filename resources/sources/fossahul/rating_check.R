# Re-run FosSahul's own quality-rating script on its own CSV and compare ratings.
# Usage: Rscript rating_check.R FOSSAHUL_CSV RATING_SCRIPT_R
# The rating script (FosSahul_Rating_updated_March2021.R) reads and writes files
# interactively; this wrapper drops those lines and the unused library(dplyr) call,
# supplies the data frame, evaluates the rest, and compares the recomputed
# preQuality and Quality with the stored columns. Base R only.

args <- commandArgs(trailingOnly = TRUE)
FosSahul <- read.csv(args[1], stringsAsFactors = FALSE)
stored_pre <- FosSahul$preQuality
stored_q <- FosSahul$Quality
code <- readLines(args[2], warn = FALSE)
drop <- grepl("^\\s*library\\(|read\\.csv\\(|file\\.choose|write\\.csv\\(", code)
cat("script lines dropped:", sum(drop), "\n")
eval(parse(text = code[!drop]))

agree <- function(a, b) sum(as.character(a) == as.character(b), na.rm = TRUE)
cat("records\t", nrow(FosSahul), "\n", sep = "")
cat("preQuality_agrees\t", agree(stored_pre, FosSahul$preQuality), "\n", sep = "")
cat("Quality_agrees\t", agree(stored_q, FosSahul$Quality), "\n", sep = "")
t <- table(stored = stored_q, recomputed = FosSahul$Quality, useNA = "ifany")
print(t)
d <- which(as.character(stored_q) != as.character(FosSahul$Quality))
if (length(d)) {
  cat("\nfirst disagreements (ID, technique, stored, recomputed, recomputed reason):\n")
  print(head(data.frame(ID = FosSahul$ID[d], tech = FosSahul$DatingTechnique[d], stored = stored_q[d],
                        recomputed = FosSahul$Quality[d], reason = FosSahul$QualityReason[d]), 15))
}

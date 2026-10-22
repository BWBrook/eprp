# Remove cross-source duplicate presences from a Triton table, conservatively.
# Usage: Rscript triton_dedup.R TRITON_RDATA OUT_TSV_GZ [PRIORITY]
#   PRIORITY: comma-separated db.source order, highest first; default is v1's
#   "ForCenS,IODP,Neptune,Pangaea,Lloydetal2012,Fentonetal2016".
# A duplicate group shares species, abundance, sample.depth and position rounded to
# 0.001 degree (v1's key, compared exactly). Only groups that have a recorded depth
# and span two or more sources are touched: the rows of the highest-priority source
# in the group are kept and the other sources' rows dropped. Within-source groups
# and rows without a depth are left alone, because most are distinct samples.
# num.ind and rel.abun are not recomputed. Prints counts. Base R only.

args <- commandArgs(trailingOnly = TRUE)
priority <- if (length(args) >= 3) strsplit(args[3], ",")[[1]] else
  c("ForCenS", "IODP", "Neptune", "Pangaea", "Lloydetal2012", "Fentonetal2016")
e <- new.env()
load(args[1], envir = e)
pres_name <- grep("\\.pres$", ls(e), value = TRUE)
stopifnot(length(pres_name) == 1, all(c("db.source", "sample.depth") %in% names(get(pres_name, envir = e))))
p <- get(pres_name, envir = e)
stopifnot(all(unique(p$db.source) %in% priority))

kd <- data.frame(p$species, p$abundance, p$sample.depth, round(p$latitude, 3), round(p$longitude, 3))
key <- do.call(paste, c(lapply(kd, function(x) format(x, digits = 17)), sep = "\r"))
gid <- match(key, unique(key))
rank <- match(p$db.source, priority)
eligible <- !is.na(p$sample.depth)
nsrc <- ave(rank, gid, FUN = function(r) length(unique(r)))
best <- ave(rank, gid, FUN = min)
drop <- eligible & nsrc > 1 & rank > best

cat("rows_in\t", nrow(p), "\n", sep = "")
cat("rows_dropped\t", sum(drop), "\n", sep = "")
t <- table(p$db.source[drop])
for (k in names(t)) cat("rows_dropped:", k, "\t", t[[k]], "\n", sep = "")
cat("rows_out\t", sum(!drop), "\n", sep = "")
out <- p[!drop, ]
nonpa <- out$abun.units != "P/A"
sums <- tapply(out$rel.abun[nonpa], out$sampleID[nonpa], sum)
cat("samples_rel_abun_sum_lt_99.9_after\t", sum(sums < 99.9, na.rm = TRUE), " of ", length(sums), "\n", sep = "")
con <- gzfile(args[2], "w")
write.table(out, con, sep = "\t", quote = FALSE, row.names = FALSE, na = "")
close(con)

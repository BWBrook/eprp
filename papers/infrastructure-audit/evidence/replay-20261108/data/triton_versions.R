args <- commandArgs(trailingOnly = TRUE)
read_presence <- function(path) {
  e <- new.env(); load(path, e)
  get(grep("\\.pres$", ls(e), value = TRUE), e)
}
v1 <- read_presence(args[1])
v3 <- read_presence(args[2])
v4 <- read_presence(args[3])
counts <- c(v1_rows = nrow(v1), v3_rows = nrow(v3), v4_rows = nrow(v4))
key <- data.frame(v1$species, v1$abundance, v1$sample.depth, round(v1$latitude, 3), round(v1$longitude, 3))
counts <- c(counts, v1_key_duplicate_excess = sum(duplicated(key)))
idx <- match(v4$rowID, v3$rowID)
stopifnot(!anyNA(idx), !anyDuplicated(v4$rowID), !anyDuplicated(v3$rowID))
changed <- v4$abun.units != v3$abun.units[idx]
counts <- c(counts, units_changed_presence = sum(changed), units_Count_to_Number_per_gram = sum(changed & v3$abun.units[idx] == "Count" & v4$abun.units == "Number per gram"))
idx <- match(v1$rowID, v4$rowID)
stopifnot(!anyNA(idx))
delta <- abs(v1$age - v4$age[idx])
fenton <- v1$db.source == "Fentonetal2016"
counts <- c(counts, shared_v1_rows = length(idx), Fenton_rows_age_change_gt_1e_6 = sum(fenton & delta > 1e-6), Fenton_max_abs_age_change_Myr = max(delta[fenton]))
write.table(data.frame(metric = names(counts), value = unname(counts)), file = args[4], sep = "\t", quote = FALSE, row.names = FALSE)

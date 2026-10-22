# Data checks on Triton RData files, testing claims in the paper, readme and code.
# Usage: Rscript triton_checks.R LABEL TRITON_RDATA [LABEL TRITON_RDATA ...]
# Prints label, check, value. Base R only.

args <- commandArgs(trailingOnly = TRUE)
say <- function(label, check, value) cat(label, "\t", check, "\t", format(value), "\n", sep = "")
for (i in seq(1, length(args), by = 2)) {
  label <- args[i]
  e <- new.env()
  load(args[i + 1], envir = e)
  pres_name <- grep("\\.pres$", ls(e), value = TRUE)
  p <- get(pres_name, envir = e)
  all <- get(sub("\\.pres$", "", pres_name), envir = e)
  say(label, "rows_all", nrow(all))
  say(label, "rows_pres", nrow(p))
  if ("trim" %in% names(p)) say(label, "trim_exc_pres", sum(p$trim == "exc"))
  # Triton's v1 record-level duplicate key (Triton_6CombinedData.R v1 l.72-76).
  if (all(c("sample.depth", "abundance") %in% names(p))) {
    key <- paste(p$species, p$abundance, p$sample.depth, round(p$latitude, 3), round(p$longitude, 3))
    say(label, "dup_rows_v1_key_lat3dp", sum(duplicated(key)))
    if ("db.source" %in% names(p)) {
      dup_keys <- unique(key[duplicated(key)])
      cross <- tapply(p$db.source[key %in% dup_keys], key[key %in% dup_keys], function(s) length(unique(s)) > 1)
      say(label, "dup_groups_spanning_sources", sum(cross))
    }
  }
  a <- p$age[!is.na(p$age) & p$age > 0]
  say(label, "ages_gt0", length(a))
  say(label, "share_ages_more_than_2dp", round(mean(abs(a * 100 - round(a * 100)) > 1e-6), 4))
  say(label, "share_ages_on_5kyr_grid", round(mean(abs(a * 200 - round(a * 200)) < 1e-6), 4))
  if ("age.err" %in% names(p)) say(label, "max_age_err", max(p$age.err, na.rm = TRUE))
  if ("age.err" %in% names(p)) say(label, "age_err_zero_share_nonorig", round(mean(p$age.err[p$age.calc != "Orig"] == 0, na.rm = TRUE), 4))
  for (sp in c("Globoconella triangula", "Globoconella sphericomiozea", "Globoconella conoidea"))
    say(label, paste0("rows_species:", sp), sum(p$species == sp))
  if ("holeID" %in% names(p)) {
    h <- p[p$holeID %in% c("SA03-1", "AMC99-1", "ST04-1", "188.1165.1165B"), ]
    t <- table(h$abun.units)
    for (k in names(t)) say(label, paste0("units_4holes:", k), t[[k]])
  }
  if ("round.age" %in% names(p)) {
    z <- p[p$round.age == 0, ]
    say(label, "share_pal_lat_eq_lat_at_round_age_0", round(mean(abs(z$pal.lat - z$latitude) < 1e-9, na.rm = TRUE), 4))
    say(label, "round_age_is_integer", all(p$round.age == round(p$round.age), na.rm = TRUE))
  }
  if ("num.ind" %in% names(p) && "total.IDd" %in% names(p)) say(label, "total_IDd_nonmissing_share", round(mean(!is.na(p$total.IDd) & p$total.IDd != ""), 4))
}

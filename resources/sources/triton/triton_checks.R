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
  # Triton's v1 record-level duplicate key (Triton_6CombinedData.R v1 l.72-76), compared exactly.
  if (all(c("sample.depth", "abundance", "db.source") %in% names(p))) {
    kd <- data.frame(p$species, p$abundance, p$sample.depth, round(p$latitude, 3), round(p$longitude, 3))
    gid <- match(do.call(paste, c(lapply(kd, function(x) format(x, digits = 17)), sep = "\r")),
                 unique(do.call(paste, c(lapply(kd, function(x) format(x, digits = 17)), sep = "\r"))))
    size <- tabulate(gid)
    in_dup <- size[gid] > 1
    say(label, "dup_rows_v1_key_exact", sum(duplicated(kd)))
    say(label, "dup_groups", sum(size > 1))
    nsrc <- tapply(p$db.source[in_dup], gid[in_dup], function(s) length(unique(s)))
    cross_g <- as.integer(names(nsrc)[nsrc > 1])
    within_g <- as.integer(names(nsrc)[nsrc == 1])
    say(label, "dup_groups_cross_source", length(cross_g))
    say(label, "dup_excess_rows_cross_source", sum(size[cross_g] - 1))
    say(label, "dup_groups_within_source", length(within_g))
    say(label, "dup_excess_rows_within_source", sum(size[within_g] - 1))
    say(label, "dup_excess_rows_with_na_depth", sum(duplicated(kd) & is.na(p$sample.depth)))
    na_g <- unique(gid[in_dup & is.na(p$sample.depth)])
    spread <- tapply(p$age[gid %in% na_g], gid[gid %in% na_g], function(a) diff(range(a)))
    say(label, "dup_groups_na_depth", length(na_g))
    say(label, "dup_groups_na_depth_age_spread_gt_0.5", sum(spread > 0.5))
    pairs <- tapply(p$db.source[gid %in% cross_g], gid[gid %in% cross_g], function(s) paste(sort(unique(s)), collapse = "+"))
    t <- sort(table(pairs), decreasing = TRUE)
    for (k in names(t)) say(label, paste0("dup_cross_source_groups:", k), t[[k]])
    # Cross-source groups only, with a recorded depth: the recipe in triton_dedup.R.
    say(label, "dup_excess_rows_cross_source_with_depth", sum(size[cross_g] - 1) - sum(duplicated(kd) & is.na(p$sample.depth) & gid %in% cross_g))
    phys <- paste(round(p$latitude, 3), round(p$longitude, 3), p$sample.depth)
    s <- unique(data.frame(sid = p$sampleID, src = p$db.source, phys = phys)[!is.na(p$sample.depth), ])
    shared <- tapply(s$src, s$phys, function(x) length(unique(x)) > 1)
    say(label, "samples_with_depth", nrow(s))
    say(label, "samples_sharing_position_depth_with_other_source", sum(s$phys %in% names(shared)[shared]))
  }
  if ("orig.species" %in% names(p)) {
    say(label, "orig_species_strings", length(unique(p$orig.species)))
    say(label, "orig_species_strings_joined", length(unique(grep(", ", p$orig.species, value = TRUE))))
    say(label, "orig_names_after_split", length(unique(trimws(unlist(strsplit(as.character(p$orig.species), ", "))))))
  }
  say(label, "rows_negative_age", sum(p$age < 0, na.rm = TRUE))
  a <- p$age[!is.na(p$age) & p$age > 0]
  say(label, "ages_gt0", length(a))
  say(label, "share_ages_more_than_2dp", round(mean(abs(a * 100 - round(a * 100)) > 1e-6), 4))
  say(label, "share_ages_on_5kyr_grid", round(mean(abs(a * 200 - round(a * 200)) < 1e-6), 4))
  if ("age.calc" %in% names(p)) for (m in sort(unique(as.character(p$age.calc)))) {
    am <- p$age[p$age.calc == m & !is.na(p$age) & p$age > 0]
    say(label, paste0("share_on_5kyr_grid:", m), round(mean(abs(am * 200 - round(am * 200)) < 1e-6), 4))
    say(label, paste0("share_on_2dp_grid:", m), round(mean(abs(am * 100 - round(am * 100)) < 1e-6), 4))
    if ("age.err" %in% names(p)) say(label, paste0("age_err_zero_share:", m), round(mean(p$age.err[p$age.calc == m] == 0), 4))
  }
  if ("age.err" %in% names(p)) say(label, "max_age_err", max(p$age.err, na.rm = TRUE))
  if ("age.err" %in% names(p)) say(label, "age_err_zero_share_nonorig", round(mean(p$age.err[p$age.calc != "Orig"] == 0, na.rm = TRUE), 4))
  for (v in c("trim", "Macro/micro", "AM.type", "age.model", "segment", "sample.type", "preservation", "processing"))
    if (v %in% names(p)) say(label, paste0("distinct_values:", v), length(unique(p[[v]])))
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

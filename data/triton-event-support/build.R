# Site-level support for within-event recovery designs (register Q-007, gate from
# literature/2026-10-09-register-checks-round1.md). Base R only. Run from the repository root:
#   Rscript data/triton-event-support/build.R
# Inputs (git-ignored, fetched and checksummed as recorded in README.md):
#   data/raw/triton/triton_update_2023.RData   (Triton v4, Figshare 10.6084/m9.figshare.13517414.v4, CC0)
#   data/raw/phansst/PhanSST_v001.csv          (EJJudd/PhanSST @ 32cc98e)

out_dir <- "data/triton-event-support"
e <- new.env()
load("data/raw/triton/triton_update_2023.RData", envir = e)
tri <- e$triton.pres
tri <- tri[tri$trim == "inc" & !is.na(tri$site) & !is.na(tri$age), ]
tri$site_num <- suppressWarnings(as.integer(gsub("[^0-9]", "", tri$site)))
tri <- tri[!is.na(tri$site_num), ]
# One row per distinct sample (site, sampleID). Metadata conflicts within a sample are counted, not resolved
# (Codex 82/1244: deduplicating on metadata as well would count conflicting rows as separate samples).
meta <- unique(tri[, c("site_num", "sampleID", "age", "age.calc", "abun.units")])
key <- paste(meta$site_num, meta$sampleID)
conflict <- tapply(seq_along(key), key, function(i) length(unique(meta$age[i])) > 1 ||
                     length(unique(meta$age.calc[i])) > 1 || length(unique(meta$abun.units[i])) > 1)
samples <- meta[!duplicated(key), ]
samples$meta_conflict <- as.logical(conflict[paste(samples$site_num, samples$sampleID)])

sst <- read.csv("data/raw/phansst/PhanSST_v001.csv")
sst <- sst[grepl("^(DSDP|ODP|IODP)", sst$SiteName) & !is.na(sst$Age), ]
sst$site_num <- suppressWarnings(as.integer(gsub("[^0-9]", "", sst$SiteName)))

# Event onsets on GTS2020 (Triton and PhanSST both use GTS2020); half-windows in Myr.
events <- data.frame(
  event = c("K-Pg (post only)", "PETM", "ETM2", "ETM3", "EOT"),
  onset = c(66.0, 56.0, 54.1, 52.8, 33.9),
  half  = c(2.0, 1.0, 0.3, 0.3, 1.0)
)
quant_units <- c("Count", "Relative abundance", "Number per gram")
min_side <- 5

rows <- list()
for (i in seq_len(nrow(events))) {
  ev <- events[i, ]
  win <- samples[samples$age >= ev$onset - ev$half & samples$age <= ev$onset + ev$half, ]
  for (s in sort(unique(win$site_num))) {
    w <- win[win$site_num == s, ]
    before <- sum(w$age > ev$onset)   # older than onset
    after <- sum(w$age <= ev$onset)
    t <- sst[sst$site_num == s & sst$Age >= ev$onset - ev$half & sst$Age <= ev$onset + ev$half, ]
    good <- t[!is.na(t$DiagenesisFlag) & t$DiagenesisFlag == 0, ]
    rows[[length(rows) + 1]] <- data.frame(
      event = ev$event, site = s, samples_older = before, samples_younger = after,
      samples_per_myr = round(nrow(w) / (2 * ev$half), 1),
      n_samples = nrow(w),
      n_zone_ages = sum(w$age.calc == "Zone"),
      n_quant_abundance = sum(w$abun.units %in% quant_units),
      n_meta_conflict = sum(w$meta_conflict),
      share_zone_ages = round(mean(w$age.calc == "Zone"), 3),
      share_quant_abundance = round(mean(w$abun.units %in% quant_units), 3),
      age_anchor_counts = paste(names(table(w$age.calc)), table(w$age.calc), sep = ":", collapse = ";"),
      abundance_unit_counts = paste(names(table(w$abun.units)), table(w$abun.units), sep = ":", collapse = ";"),
      temp_older = sum(t$Age > ev$onset), temp_younger = sum(t$Age <= ev$onset),
      temp_good_older = sum(good$Age > ev$onset), temp_good_younger = sum(good$Age <= ev$onset),
      temp_proxies = paste(sort(unique(t$ProxyType)), collapse = "+")
    )
  }
}
res <- do.call(rbind, rows)
res$biota_ok <- (res$samples_older >= min_side | res$event == "K-Pg (post only)") & res$samples_younger >= min_side
# Thresholds use unrounded counts (Codex 82/1244); share columns are for display only.
res$ages_ok <- res$n_zone_ages / res$n_samples < 0.5
res$temp_ok <- res$temp_older >= 3 & res$temp_younger >= 3
res$temp_good_ok <- res$temp_good_older >= 3 & res$temp_good_younger >= 3
write.table(res, file.path(out_dir, "event_sites.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)

summ <- do.call(rbind, lapply(split(res, res$event), function(d) data.frame(
  event = d$event[1],
  sites_any = nrow(d),
  biota = sum(d$biota_ok),
  biota_nonzone = sum(d$biota_ok & d$ages_ok),
  biota_nonzone_quant = sum(d$biota_ok & d$ages_ok & d$n_quant_abundance / d$n_samples >= 0.5),
  plus_temp = sum(d$biota_ok & d$ages_ok & d$temp_ok),
  plus_temp_good = sum(d$biota_ok & d$ages_ok & d$temp_good_ok),
  gate_sites = paste(d$site[d$biota_ok & d$ages_ok & d$temp_ok], collapse = ",")
)))
summ <- summ[match(events$event, summ$event), ]
write.table(summ, file.path(out_dir, "event_summary.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
print(summ, row.names = FALSE)

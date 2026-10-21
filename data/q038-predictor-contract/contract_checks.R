# Q-038 replacement contract: deterministic checks cited by contract.md. Base R; no fitting of the deposit.
# Run from the repository root:  Rscript --vanilla data/q038-predictor-contract/contract_checks.R
# Outputs (tracked): contract_checks.tsv (one named value per row), prefix_features_check.tsv, exposure.tsv
#   E1  prefix invariance: retrospective membership changes with the future; the prefix rule and forecasts do not
#   E2  Codex's two-genus detection-only example (76/2112): observation gain without biological selectivity
#   E3  identification by exact expected log-likelihood: naive last appearance, joint CJS, and a non-identified case
#   E4  prefix-learned clade labels cannot be outvoted by future references; full-archive labels can
#   P   prefix-invariance of every forecast feature on the deposit, under three perturbations of the future
raw <- "data/raw/monarrez2023"
out <- "data/q038-predictor-contract"
res <- list()
put <- function(name, value) res[[name]] <<- value
logit <- function(p) log(p / (1 - p)); expit <- function(x) 1 / (1 + exp(-x))

# ---- CJS history probability (first record at stage 1 conditioned on) ---------------------------------------------
# y: detections at stages 2..T; phi[t]: survival t -> t+1 (t = 1..T-1); p[t]: detection at stage t (t = 2..T; p[1] unused)
hist_probs <- function(H, phi, p) {                                 # all rows of H at once
  a <- rep(1, nrow(H)); d <- rep(0, nrow(H))
  for (t in 2:(ncol(H) + 1)) {
    an <- a * phi[t - 1]; dn <- d + a * (1 - phi[t - 1]); y <- H[, t - 1]
    a <- ifelse(y == 1, an * p[t], an * (1 - p[t])); d <- ifelse(y == 1, 0, dn)
  }
  a + d
}
histories <- function(n) as.matrix(expand.grid(rep(list(0:1), n)))[, n:1, drop = FALSE]

# ---- E1: prefix invariance on enumerated histories ----------------------------------------------------------------
# One genus, first record at stage 1, T = 6, event stage k = 4 (prefix = stages 1..3, forecast origin end of stage 3).
k <- 4; Tn <- 6; W <- 3
phi <- c(.9, .9, .9, .6, .9); pdet <- c(NA, .5, .5, .5, .5, .5)
H <- histories(Tn - 1)                                              # columns = stages 2..6
retro <- apply(H, 1, function(y) max(c(1, which(y == 1) + 1)) >= k)  # fad < k <= lad (range-through)
forecast <- function(y) {                                           # uses stages 1..k-1 only
  pre <- c(1, y[1:(k - 2)]); l <- max(which(pre == 1))
  inR <- l >= k - W
  num <- prod(phi[l:(k - 1)]) * prod(1 - pdet[seq_len(k - 1)[seq_len(k - 1) > l]])
  chi <- function(t) if (t == k - 1) 1 else (1 - phi[t]) + phi[t] * (1 - pdet[t + 1]) * chi(t + 1)
  pi_k <- num / chi(l)
  c(inR = inR, l = l, pi_k = pi_k, lambda = pi_k * (1 - phi[k]))
}
F <- t(apply(H, 1, forecast))
pref <- apply(H[, 1:(k - 2), drop = FALSE], 1, paste, collapse = "")
by_prefix <- split(seq_len(nrow(H)), pref)
put("E1_prefixes", length(by_prefix))
put("E1_prefixes_where_retrospective_membership_varies", sum(sapply(by_prefix, function(i) length(unique(retro[i])) > 1)))
put("E1_prefixes_where_forecast_varies", sum(sapply(by_prefix, function(i) nrow(unique(F[i, , drop = FALSE])) > 1)))
# Codex's 76/2112 pair at k = 2: histories 1,0,0 and 1,0,1 share the stage-1 prefix but differ in range-through
# membership at stage 2 (lad >= 2 only for the second).
put("E1_codex_pair_membership_100", max(which(c(1, 0, 0) == 1)) >= 2)
put("E1_codex_pair_membership_101", max(which(c(1, 0, 1) == 1)) >= 2)

# ---- E2: two-genus detection-only example ---------------------------------------------------------------------------
# Equal biological loss .2; survivor post-boundary detection .2 and .8; exactly one observed loss.
qo <- c(.2 + .8 * .8, .2 + .8 * .2)                                 # observed-loss probabilities .84, .36
pv <- c(qo[1] * (1 - qo[2]), qo[2] * (1 - qo[1])); pv <- pv / sum(pv)
put("E2_observed_loss_probs", paste(qo, collapse = ","))
put("E2_P_low_detection_is_victim", pv[1])
put("E2_observation_gain_nats", sum(pv * (log(pv) - log(.5))))
put("E2_biological_gain_nats", 0)                                   # equal eta: Fisher set model is uniform

# ---- E3: identification by exact expected log-likelihood --------------------------------------------------------------
# Two equally common types, L (low detectability) and H. Stages 1..k-1 = 1..3 prefix, event stage k = 4 (transition
# 4 -> 5 carries the event), then M post-event stages. Background survival .9; event loss logit = alpha + beta * [L].
truth <- function(beta, M) list(phib = .9, alpha = logit(.4), beta = beta, p = c(L = .3, H = .8), M = M)
type_params <- function(th, g, M, ppost = NULL) {
  Tn <- 4 + M
  phi <- rep(th$phib, Tn - 1); phi[4] <- 1 - expit(th$alpha + th$beta * (g == "L"))
  p <- rep(th$p[[g]], Tn); if (!is.null(ppost)) p[5:Tn] <- ppost[[g]]
  list(phi = phi, p = p, Tn = Tn)
}
dist <- function(th, M, ppost = NULL) lapply(c(L = "L", H = "H"), function(g) {
  tp <- type_params(th, g, M, ppost); Hh <- histories(tp$Tn - 1)
  list(H = Hh, P = hist_probs(Hh, tp$phi, tp$p))
})
naive <- function(D, M) {                                           # what last-appearance analyses would report
  sapply(D, function(d) {
    lad <- apply(d$H, 1, function(y) max(c(1, which(y == 1) + 1)))
    coh <- lad >= 4                                                 # retrospective cohort, fad = 1 < k = 4 <= lad
    post <- apply(d$H[, 4:(3 + M), drop = FALSE], 1, function(y) any(y == 1))   # recorded at stages 5..4+M
    c(retro = sum(d$P[coh & lad == 4]) / sum(d$P[coh]), prefix_obs = 1 - sum(d$P[post]))
  })
}
ell <- function(D, th, M, ppost = NULL) {                           # expected log-likelihood, equal type weights
  sum(sapply(c("L", "H"), function(g) {
    tp <- type_params(th, g, M, ppost)
    .5 * sum(D[[g]]$P * log(hist_probs(D[[g]]$H, tp$phi, tp$p)))
  }))
}
unpack <- function(v, free_post) {
  th <- list(phib = expit(v[1]), alpha = v[2], beta = v[3], p = c(L = expit(v[4]), H = expit(v[5])))
  list(th = th, ppost = if (free_post) c(L = expit(v[6]), H = expit(v[7])) else NULL)
}
fit <- function(D, M, free_post, beta_fixed = NULL) {
  f <- function(v) { if (!is.null(beta_fixed)) v <- append(v, beta_fixed, 2); u <- unpack(v, free_post); -ell(D, u$th, M, u$ppost) }
  n <- 5 + 2 * free_post - !is.null(beta_fixed)
  best <- NULL
  for (s in 1:4) {
    set.seed(s); v0 <- rnorm(n, 0, .5)
    o <- optim(v0, f, method = "BFGS", control = list(reltol = 1e-15, maxit = 5000))
    if (is.null(best) || o$value < best$value) best <- o
  }
  best
}
for (sc in list(list(name = "null", beta = 0), list(name = "positive", beta = 1))) {
  for (M in c(1, 3)) {
    D <- dist(truth(sc$beta, M), M)
    nv <- naive(D, M)
    put(sprintf("E3_%s_M%d_naive_retrospective_logOR_L_vs_H", sc$name, M), logit(nv["retro", "L"]) - logit(nv["retro", "H"]))
    put(sprintf("E3_%s_M%d_naive_prefix_observation_logOR_L_vs_H", sc$name, M), logit(nv["prefix_obs", "L"]) - logit(nv["prefix_obs", "H"]))
    o <- fit(D, M, free_post = FALSE)
    put(sprintf("E3_%s_M%d_joint_constant_detection_beta_hat", sc$name, M), o$par[3])
    dc <- sapply(c(-.5, .5), function(db) fit(D, M, free_post = FALSE, beta_fixed = sc$beta + db)$value - o$value)
    put(sprintf("E3_%s_M%d_constant_detection_profile_drops", sc$name, M), paste(signif(dc, 4), collapse = ","))
    # Per-genus information from the mean drop at |dbeta| = .5, and the implied standard error for N genera.
    info <- 2 * mean(dc) / .25
    put(sprintf("E3_%s_M%d_constant_detection_SE_beta_N100_N200", sc$name, M), paste(signif(1 / sqrt(info * c(100, 200)), 3), collapse = ","))
    o2 <- fit(D, M, free_post = TRUE)
    put(sprintf("E3_%s_M%d_joint_free_post_detection_beta_hat", sc$name, M), o2$par[3])
    # Profile: best expected log-likelihood with beta held at truth +/- .5, relative to the unrestricted maximum.
    df <- sapply(c(-.5, .5), function(db) fit(D, M, free_post = TRUE, beta_fixed = sc$beta + db)$value - o2$value)
    put(sprintf("E3_%s_M%d_free_post_profile_drops", sc$name, M), paste(signif(df, 4), collapse = ","))
    if (M == 3) put(sprintf("E3_%s_M%d_free_post_SE_beta_N100_N200", sc$name, M),
                    paste(signif(1 / sqrt(2 * mean(df) / .25 * c(100, 200)), 3), collapse = ","))
  }
}

# ---- E4: prefix-learned labels ------------------------------------------------------------------------------------------
modal <- function(labels, refs) {
  keep <- !is.na(labels) & labels != ""
  if (!any(keep)) return("unknown")
  n <- tapply(refs[keep], labels[keep], function(r) length(unique(r)))
  top <- names(n)[n == max(n)]
  if (length(top) > 1) "unresolved" else top
}
lab <- data.frame(s = c(1, 2, 5, 6, 6), family = c("A", "A", "B", "B", "B"), ref = 1:5)
put("E4_full_archive_label", modal(lab$family, lab$ref))
put("E4_prefix_label_cutoff_k4", with(lab[lab$s <= 3, ], modal(family, ref)))

# ---- P: prefix-invariance of forecast features on the deposit ---------------------------------------------------------
classes <- c("Rhynchonellata", "Bivalvia")
events <- c(LOME = 7, LD = 21, EP = 38, ETr = 45, KPg = 68)
occ <- read.csv(file.path(raw, "pbdb.cleaned.classes.csv"))
o <- occ[occ$class %in% classes, ]
bases <- sort(unique(o$max_ma), decreasing = TRUE)
o$s <- match(o$max_ma, bases)
stg <- unique(o[, c("s", "max_ma", "min_ma")]); stg <- stg[order(stg$s), ]

gc_max <- function(lat, lng) {
  p <- unique(cbind(lat, lng))
  if (nrow(p) < 2) return(0)
  r <- pi / 180; la <- p[, 1] * r; lo <- p[, 2] * r; m <- 0
  for (i in seq_len(nrow(p) - 1)) {
    j <- (i + 1):nrow(p)
    a <- sin((la[j] - la[i]) / 2)^2 + cos(la[i]) * cos(la[j]) * sin((lo[j] - lo[i]) / 2)^2
    m <- max(m, 2 * 6371 * asin(pmin(1, sqrt(a))))
  }
  m
}
zs <- function(v) { m <- mean(v, na.rm = TRUE); s <- sd(v, na.rm = TRUE); if (all(is.na(v))) v else if (is.na(s) || s == 0) ifelse(is.na(v), NA, 0) else (v - m) / s }

# Every quantity is computed from rows with s <= k - 1 after the first line; nothing later is reachable.
prefix_features <- function(occ_c, k, W = 3) {
  x <- occ_c[occ_c$s <= k - 1, ]
  fam <- tapply(seq_len(nrow(x)), x$genus_no, function(i) modal(x$family[i], x$reference_no[i]))
  x$fam <- fam[as.character(x$genus_no)]
  ordf <- tapply(seq_len(nrow(x)), x$fam, function(i) modal(x$order[i], x$reference_no[i]))
  g <- split(x, x$genus_no)
  F <- do.call(rbind, lapply(g, function(y) {
    l <- max(y$s); f <- min(y$s); yl <- y[y$s == l, ]; loc <- !is.na(yl$paleolat) & !is.na(yl$paleolng)
    fm <- y$fam[1]
    data.frame(genus_no = y$genus_no[1], first = f, last_prefix = l, in_risk_set = l >= k - W,
               recency_stages = k - 1 - l, recency_myr = stg$min_ma[l] - stg$min_ma[k - 1],
               age_myr = stg$max_ma[f] - stg$min_ma[k - 1],
               refs_last = length(unique(yl$reference_no)), colls_last = length(unique(yl$collection_no)),
               located_rows_last = sum(loc), located_pairs_last = nrow(unique(cbind(yl$paleolat, yl$paleolng)[loc, , drop = FALSE])),
               range_km_last = if (any(loc)) gc_max(yl$paleolat[loc], yl$paleolng[loc]) else NA,
               completeness = length(unique(y$s)) / (l - f + 1),
               family = fm, order = if (fm %in% c("unknown", "unresolved")) modal(y$order, y$reference_no) else ordf[[fm]])
  }))
  R <- F[F$in_risk_set, ]
  for (v in c("recency_myr", "age_myr", "completeness")) R[[paste0("z_", v)]] <- zs(R[[v]])
  for (v in c("refs_last", "colls_last")) R[[paste0("z_log_", v)]] <- zs(log(R[[v]]))
  R$z_log_range <- zs(log10(R$range_km_last + 1))
  R[order(R$genus_no), ]
}
perturb <- function(occ_c, k, how) {
  fut <- occ_c$s >= k
  if (how == "delete_future") return(occ_c[!fut, ])
  if (how == "shuffle_future_stages") { set.seed(k); occ_c$s[fut] <- sample(occ_c$s[fut]); return(occ_c) }
  if (how == "inject_future_labels") {           # many later references relabelling 50 prefix genera
    set.seed(k); gs <- sample(unique(occ_c$genus_no[occ_c$s <= k - 1]), 50)
    add <- occ_c[match(rep(gs, each = 5), occ_c$genus_no), ]
    add$s <- as.integer(k + 1); add$family <- "Injectedidae"; add$order <- "Injectida"; add$reference_no <- -seq_len(nrow(add))
    return(rbind(occ_c, add))
  }
}
pf <- list()
for (cl in classes) for (ev in names(events)) {
  k <- events[[ev]]; oc <- o[o$class == cl, ]
  base <- prefix_features(oc, k)
  for (how in c("delete_future", "shuffle_future_stages", "inject_future_labels")) {
    pf[[length(pf) + 1]] <- data.frame(class = cl, event = ev, k = k, perturbation = how, risk_set = nrow(base),
                                       identical = identical(base, prefix_features(perturb(oc, k, how), k)))
  }
}
pf <- do.call(rbind, pf)
write.table(pf, file.path(out, "prefix_features_check.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
put("P_all_identical", all(pf$identical))

# Exposure series for the detection model: distinct references per stage, by focal class and for the other six
# deposited classes (a sampling-opportunity sensitivity that does not use the focal class's own records).
ex <- do.call(rbind, lapply(seq_len(nrow(stg)), function(t) {
  a <- occ[match(occ$max_ma, bases) %in% t, ]
  data.frame(s = t, base_ma = stg$max_ma[t],
             refs_Rhynchonellata = length(unique(a$reference_no[a$class == "Rhynchonellata"])),
             refs_Bivalvia = length(unique(a$reference_no[a$class == "Bivalvia"])),
             refs_other_classes = length(unique(a$reference_no[!(a$class %in% classes)])))
}))
write.table(ex, file.path(out, "exposure.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

kv <- data.frame(name = names(res), value = vapply(res, function(v) if (is.numeric(v)) format(signif(v, 7)) else as.character(v), ""))
write.table(kv, file.path(out, "contract_checks.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(kv, row.names = FALSE)
print(pf, row.names = FALSE)

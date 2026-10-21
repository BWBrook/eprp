# Q-038 contract v2: deterministic checks for Codex's 76/2153 amendments, cited by contract.md sections 3-5.
# Base R; synthetic enumerations only; no deposit fit.
# Run from the repository root:  Rscript --vanilla data/q038-predictor-contract/contract_checks_v2.R
# Output (tracked): contract_checks_v2.tsv (one named value per row)
#   S  the observation score law: conditioning after integration, normalisation, endpoints, no severity root
#   M  leave-one-event-out masking: every component crossing the held-out transition is cut, unseen tails included
#   F  epsilon = .5 final-stage exposure: pair-state likelihood with tilted first-capture conditioning
out <- "data/q038-predictor-contract"
res <- list()
put <- function(name, value) res[[name]] <<- value

# ---- S: score law --------------------------------------------------------------------------------------------------
pset <- function(q, S) prod(ifelse(seq_along(q) %in% S, q, 1 - q))
subsets <- function(n, D) if (D == 0) list(integer(0)) else combn(n, D, simplify = FALSE)
# Codex's two-draw mixture (76/2153): draws A and B equally weighted, two genera, observed loss set {1}, D = 1.
qA <- c(.9, .8); qB <- c(.4, .1); S <- 1
cond <- function(q, S, D) pset(q, S) / sum(sapply(subsets(length(q), D), function(s) pset(q, s)))
proper <- (pset(qA, S) + pset(qB, S)) / (sum(sapply(subsets(2, 1), function(s) pset(qA, s))) + sum(sapply(subsets(2, 1), function(s) pset(qB, s))))
put("S1_mixture_conditional_after_integration", proper)
put("S1_average_of_conditionals", (cond(qA, S, 1) + cond(qB, S, 1)) / 2)
put("S1_conditional_of_averaged_q", cond((qA + qB) / 2, S, 1))
# Normalisation over all sets of each size, for the adopted law, on a 4-genus, 3-draw mixture with unequal weights.
set.seed(38); Q <- matrix(runif(12, .05, .95), 3); wts <- c(.5, .3, .2)
law <- function(S, D) sum(wts * apply(Q, 1, pset, S = S)) / sum(wts * apply(Q, 1, function(q) sum(sapply(subsets(4, D), function(s) pset(q, s)))))
put("S2_max_normalisation_error_over_D", max(sapply(0:4, function(D) abs(sum(sapply(subsets(4, D), law, D = D)) - 1))))
put("S2_endpoint_D0_probability", law(integer(0), 0))
put("S2_endpoint_DN_probability", law(1:4, 4))
put("S2_unconditional_total", sum(sapply(0:4, function(D) sum(sapply(subsets(4, D), function(s) sum(wts * apply(Q, 1, pset, S = s)))))))
# No-root example (76/2153): membership .2/.4 and post-boundary detection .8 for both; with no event deaths the smallest
# achievable expected observed loss exceeds a possible D_O = 1, so solving sum(q) = D_O for severity has no root.
pis <- c(.2, .4); r <- c(.8, .8)
put("S3_min_sum_q_without_event_deaths", sum(1 - pis * r))
put("S3_P_DO_equals_1_at_zero_event_loss", sum(sapply(subsets(2, 1), function(s) pset(1 - pis * r, s))))

# ---- M: masking for leave-one-event-out ----------------------------------------------------------------------------
# CJS component likelihood: first record f (conditioned), records y[t] for t in f..C, censoring at C (chi_C = 1).
comp_lik <- function(y, f, C, phi, p) {
  if (C <= f) return(1)
  obs <- which(y[f:C] == 1) + f - 1; l <- max(obs)
  L <- if (l > f) prod(phi[f:(l - 1)]) * prod(ifelse(y[(f + 1):l] == 1, p[(f + 1):l], 1 - p[(f + 1):l])) else 1
  chi <- 1
  if (l < C) for (t in (C - 1):l) chi <- (1 - phi[t]) + phi[t] * (1 - p[t + 1]) * chi
  L * chi
}
# Masked likelihood for held-out event stage ks (transition ks -> ks + 1) and the held-out risk set.
masked_lik <- function(y, phi, p, ks, heldout) {
  Tn <- length(y); f <- min(which(y == 1))
  if (f > ks) return(comp_lik(y, f, Tn, phi, p))                     # enters after the boundary: untouched
  left <- comp_lik(y, f, if (heldout) ks - 1 else ks, phi, p)         # left component, censored before the transition
  if (heldout || !any(y[(ks + 1):Tn] == 1)) return(left)              # held-out futures masked; no restart without a record
  f2 <- ks + min(which(y[(ks + 1):Tn] == 1))
  left * comp_lik(y, f2, Tn, phi, p)                                  # restart on the first post-boundary record
}
spanning_only <- function(y, phi, p, ks) {                            # the rejected rule: cut only if seen on both sides
  Tn <- length(y); f <- min(which(y == 1))
  seen_after <- any(y[(ks + 1):Tn] == 1)
  if (f <= ks && seen_after) return(masked_lik(y, phi, p, ks, FALSE))
  comp_lik(y, f, Tn, phi, p)
}
Tn <- 7; ks <- 4; p <- c(1, .22, .71, .43, .81, .32, .63)
phi_with <- function(e) { v <- c(.83, .72, .91, .58, .86, .79); v[ks] <- e; v }
cases <- list(old_never_reappears = c(1, 0, 0, 0, 0, 0, 0), bridging_gap = c(1, 1, 0, 0, 0, 1, 0),
              entrant_at_ks = c(0, 0, 0, 1, 0, 1, 1), recent_spanning = c(0, 1, 1, 1, 1, 0, 1),
              late_entrant = c(0, 0, 0, 0, 1, 1, 0))
# Codex's example (76/2153): survival .9 except the held-out transition, detection .5 after stage 1.
phi_c <- function(e) { v <- rep(.9, 6); v[ks] <- e; v }; p_c <- c(1, rep(.5, 6))
put("M1_codex_old_genus_full_lik_phi.9", comp_lik(cases$old_never_reappears, 1, Tn, phi_c(.9), p_c))
put("M1_codex_old_genus_full_lik_phi.2", comp_lik(cases$old_never_reappears, 1, Tn, phi_c(.2), p_c))
put("M1_codex_old_genus_masked_range", diff(range(sapply(c(.9, .2), function(e) masked_lik(cases$old_never_reappears, phi_c(e), p_c, ks, FALSE)))))
for (nm in names(cases)) {
  y <- cases[[nm]]
  put(sprintf("M2_%s_masked_varies_with_event_phi", nm), diff(range(sapply(c(.05, .5, .95), function(e) masked_lik(y, phi_with(e), p, ks, FALSE)))) > 0)
  put(sprintf("M2_%s_spanning_only_varies_with_event_phi", nm), diff(range(sapply(c(.05, .5, .95), function(e) spanning_only(y, phi_with(e), p, ks)))) > 0)
}
# Held-out risk-set genus: its masked contribution must not change with any future record pattern.
pre <- c(1, 0, 1)                                                     # stages 1..3, last prefix record at k* - 1
fut <- as.matrix(expand.grid(rep(list(0:1), Tn - 3)))
vals <- apply(fut, 1, function(z) masked_lik(c(pre, z), phi_with(.5), p, ks, TRUE))
put("M3_heldout_genus_futures_enumerated", nrow(fut))
put("M3_heldout_genus_masked_range_over_futures", diff(range(vals)))
put("M3_heldout_genus_masked_range_over_event_phi", diff(range(sapply(c(.05, .5, .95), function(e) masked_lik(c(pre, 0, 1, 1, 0), phi_with(e), p, ks, TRUE)))))
# Every restarted component is a proper conditional law: probabilities of all continuations after a first record sum to 1.
tot <- sum(apply(as.matrix(expand.grid(rep(list(0:1), Tn - 5))), 1, function(z) comp_lik(c(0, 0, 0, 0, 1, z), 5, Tn, phi_with(.5), p)))
put("M4_restart_component_total_probability", tot)

# ---- F: epsilon = .5 in the final stage alive ----------------------------------------------------------------------
# Emission in stage t depends on whether the genus dies during t: p_eps = 1 - (1 - p)^eps (eps applied to exposure).
# Joint over (alive_t, dies_in_t). First-capture conditioning: given detection at f, survival out of f is tilted:
#   P(z_{f+1} = 1 | detected at f) = phi_f p_f / (phi_f p_f + (1 - phi_f) p_eps_f).
lik_eps <- function(y, f, phi, p, eps) {                             # P(y_{f+1..T} | first record at f), by enumeration
  Tn <- length(y); pe <- 1 - (1 - p)^eps
  tot <- 0
  for (dstage in f:Tn) {                                              # last stage alive (Tn = survives to the end)
    pr <- if (dstage < Tn) prod(phi[f:dstage][-length(f:dstage)]) * (1 - phi[dstage]) else prod(phi[f:(Tn - 1)])
    if (dstage == f && dstage < Tn) pr <- 1 - phi[f]
    em <- 1
    for (t in f:Tn) {
      alive <- t <= dstage
      pt <- if (!alive) 0 else if (t == dstage && dstage < Tn) pe[t] else p[t]
      if (t == f) { em <- em * pt; next }                             # the first record itself
      em <- em * (if (y[t] == 1) pt else 1 - pt)
    }
    tot <- tot + pr * em
  }
  pf <- phi[f] * p[f] + (1 - phi[f]) * pe[f]                          # P(detected at f | alive at f)
  if (f == Tn) pf <- p[f]
  tot / pf
}
p2 <- c(.6, .22, .71, .43, .81, .32, .63)
H <- as.matrix(expand.grid(rep(list(0:1), Tn - 1)))
for (eps in c(1, .5)) {
  s <- sum(apply(H, 1, function(z) lik_eps(c(1, z), 1, phi_with(.58), p2, eps)))
  put(sprintf("F1_eps%.1f_total_probability_after_first_capture", eps), s)
}
put("F2_eps1_matches_standard_CJS_max_abs", max(apply(H, 1, function(z) abs(lik_eps(c(1, z), 1, phi_with(.58), p2, 1) - comp_lik(c(1, z), 1, Tn, phi_with(.58), p2)))))
put("F3_tilted_first_survival_eps.5", phi_with(.58)[1] * p2[1] / (phi_with(.58)[1] * p2[1] + (1 - phi_with(.58)[1]) * (1 - (1 - p2[1])^.5)))
put("F3_untilted_first_survival", phi_with(.58)[1])

# ---- T: asymmetric leave-one-event-out labels and features on the deposit --------------------------------------------
# Held-out genera (the prefix risk set of k*) lose every row from stage k* on. Other genera keep all rows: their later
# records may resolve family-to-order mappings (declared retrospective-transport information). Held-out genera's
# features, labels and standardising constants must not change when their own future rows change.
modal <- function(labels, refs) {
  keep <- !is.na(labels) & labels != ""
  if (!any(keep)) return("unknown")
  n <- tapply(refs[keep], labels[keep], function(r) length(unique(r)))
  top <- names(n)[n == max(n)]
  if (length(top) > 1) "unresolved" else top
}
zs <- function(v) { m <- mean(v, na.rm = TRUE); s <- sd(v, na.rm = TRUE); if (all(is.na(v))) v else if (is.na(s) || s == 0) ifelse(is.na(v), NA, 0) else (v - m) / s }
occ <- read.csv("data/raw/monarrez2023/pbdb.cleaned.classes.csv")
o <- occ[occ$class %in% c("Rhynchonellata", "Bivalvia"), ]
o$s <- match(o$max_ma, sort(unique(o$max_ma), decreasing = TRUE))
risk_ids <- function(oc, k, W = 3) { x <- oc[oc$s <= k - 1, ]; l <- tapply(x$s, x$genus_no, max); as.integer(names(l)[l >= k - W]) }
loeo_features <- function(oc, k, R) {
  adm <- oc[!(oc$genus_no %in% R & oc$s >= k), ]
  fam <- tapply(seq_len(nrow(adm)), adm$genus_no, function(i) modal(adm$family[i], adm$reference_no[i]))
  adm$fam <- fam[as.character(adm$genus_no)]
  ordf <- tapply(seq_len(nrow(adm)), adm$fam, function(i) modal(adm$order[i], adm$reference_no[i]))
  x <- adm[adm$genus_no %in% R, ]
  F <- do.call(rbind, lapply(split(x, x$genus_no), function(y) {
    l <- max(y$s); yl <- y[y$s == l, ]; fm <- y$fam[1]
    data.frame(genus_no = y$genus_no[1], last_prefix = l, refs_last = length(unique(yl$reference_no)),
               completeness = length(unique(y$s)) / (l - min(y$s) + 1), family = fm,
               order = if (fm %in% c("unknown", "unresolved")) modal(y$order, y$reference_no) else ordf[[fm]])
  }))
  F$z_log_refs <- zs(log(F$refs_last)); F$z_completeness <- zs(F$completeness)
  F[order(F$genus_no), ]
}
pert <- function(oc, k, R, how, who) {
  tgt <- oc$s >= k & (if (who == "heldout") oc$genus_no %in% R else !(oc$genus_no %in% R))
  if (how == "delete") return(oc[!tgt, ])
  set.seed(k)
  if (how == "shuffle") { oc$s[tgt] <- sample(oc$s[tgt]); return(oc) }
  gs <- sample(unique(oc$genus_no[tgt]), min(50, length(unique(oc$genus_no[tgt]))))
  add <- oc[match(rep(gs, each = 5), oc$genus_no), ]; add$s <- as.integer(k + 1)
  fams <- unique(oc$family[oc$genus_no %in% R & oc$family != ""])
  add$family <- if (who == "heldout") "Injectedidae" else sample(fams, nrow(add), replace = TRUE)
  add$order <- "Injectida"; add$reference_no <- -seq_len(nrow(add))
  rbind(oc, add)
}
tc <- list()
for (cl in c("Rhynchonellata", "Bivalvia")) for (k in c(7, 21, 38, 45, 68)) {
  oc <- o[o$class == cl, ]; R <- risk_ids(oc, k); base <- loeo_features(oc, k, R)
  for (how in c("delete", "shuffle", "inject")) {
    tc[[length(tc) + 1]] <- data.frame(class = cl, k = k, perturbation = how, heldout_future_rows_changed = TRUE,
                                       identical = identical(base, loeo_features(pert(oc, k, R, how, "heldout"), k, R)))
  }
  tc[[length(tc) + 1]] <- data.frame(class = cl, k = k, perturbation = "inject_other_genera_orders", heldout_future_rows_changed = FALSE,
                                     identical = identical(base, loeo_features(pert(oc, k, R, "inject", "other"), k, R)))
}
tc <- do.call(rbind, tc)
write.table(tc, file.path(out, "loeo_features_check.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
put("T1_heldout_future_perturbations_identical", sum(tc$identical[tc$heldout_future_rows_changed]))
put("T1_heldout_future_perturbations_total", sum(tc$heldout_future_rows_changed))
put("T2_other_genera_later_labels_change_heldout_features", sum(!tc$identical[!tc$heldout_future_rows_changed]))

kv <- data.frame(name = names(res), value = vapply(res, function(v) if (is.numeric(v)) format(signif(v, 10)) else as.character(v), ""))
write.table(kv, file.path(out, "contract_checks_v2.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(kv, row.names = FALSE)

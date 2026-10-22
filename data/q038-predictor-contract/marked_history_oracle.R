# Q-038 contract v3: exact marked-history oracle (Codex 76/2166, review 2026-10-22). Base R; synthetic only.
# Run from the repository root:  Rscript --vanilla data/q038-predictor-contract/marked_history_oracle.R
# Output (tracked): marked_history_oracle.tsv
#   O1 Codex's example: integrating the unseen stage-k count gives q = .6686076997; freezing predictors gives .6852245278
#   O2 the predictive function integrates future marks exactly for small exposure; total probability and set/count laws
#   O3 with scaling frozen at the origin, the two-genus joint law factorises; re-standardising future risk sets does not
#   O4 the predictive uses the prefix only: replacing held-out realised records leaves it unchanged
#   O5 Monte Carlo integration (for realistic exposure) agrees with exact enumeration within its error
#   O6 entry and first capture: the generator's first-capture count law and the epsilon tilt, by enumeration
#   O7 epsilon = .5 masking: cutting left components at k-1 removes the event dependence that a cut at k retains
out <- "data/q038-predictor-contract"
res <- list(); put <- function(n, v) res[[n]] <<- v

# ---- the model pieces shared by generator and predictor --------------------------------------------------------------
# Reference-level detection: each of E_t references detects a living genus with r = 1 - exp(-theta); the count is
# Binomial(E_t, r); a stage is recorded when the count is positive. theta = theta0 * (mean references per recorded
# stage before t)^gw, i.e. log theta = log theta0 + gw * w with w the log mean (w = 0 before any record).
# Hazard: logit(1 - phi_t) = alpha_t + beta_t * x_t, x_t = (log refs at the last recorded stage before t - mu0) / s0,
# with mu0 and s0 FROZEN at the forecast origin (policy declared in contract.md section 4).
theta_of <- function(counts, theta0, gw) { rec <- counts[counts > 0]; if (!length(rec)) theta0 else theta0 * mean(rec)^gw }
x_of <- function(counts, mu0, s0) { rec <- counts[counts > 0]; if (!length(rec)) 0 else (log(rec[length(rec)]) - mu0) / s0 }
# The hazard covariate for the transition (t - 1 -> t) uses stages before t - 1 (contract section 3: stages < s for s -> s + 1).
x_tr <- function(counts, t, mu0, s0) x_of(counts[seq_len(t - 2)], mu0, s0)

# Exact predictive q = P(no record in stages k+1..k+M | prefix) for one genus, integrating stage k..k+M counts.
# prefix: counts at stages 1..k-1 (first record in the prefix); E: exposure by stage; alive_k1: P(alive at k-1 | prefix)
# is supplied by the caller (membership filter, unchanged from v1); alpha, beta by transition index t (t -> t+1).
predict_q_exact <- function(prefix, E, k, M, alive_k1, alpha, beta, theta0, gw, mu0, s0, frozen = FALSE) {
  rec_paths <- function(counts, t, alive, pr) {   # recursion over stages t..k+M; returns P(no record in k+1..k+M)
    if (t > k + M) return(pr)
    if (!alive) return(pr)                        # dead: no further records
    xc <- if (frozen) prefix else counts
    phi <- 1 - plogis(alpha[t - 1] + beta[t - 1] * (if (frozen) x_of(prefix, mu0, s0) else x_tr(counts, t, mu0, s0)))
    tot <- pr * (1 - phi) * 1                       # dies before t: no records at t..k+M
    th <- theta_of(xc, theta0, gw)
    r <- 1 - exp(-th)
    for (cc in 0:E[t]) {
      pc <- dbinom(cc, E[t], r)
      if (t > k && cc > 0) next                      # a record in the observation window: excluded from q
      tot <- tot + rec_paths(c(counts, cc), t + 1, TRUE, pr * phi * pc)
    }
    tot
  }
  # alive at k-1 with probability alive_k1; dead before k gives q contribution 1
  (1 - alive_k1) + rec_paths(prefix, k, TRUE, alive_k1)
}

# ---- O1: Codex's example ----------------------------------------------------------------------------------------------
# Prefix: one recorded stage with one reference; theta = .5 * mean refs; E_k = 2, E_{k+1} = 1; membership one;
# event survival .8 (k -> k+1); observation window k+1 only (M = 1). Stage k-1 -> k survival is 1 here.
k <- 3; M <- 1
E <- c(1, 1, 2, 1)
alpha <- c(-Inf, -Inf, qlogis(.2)); beta <- c(0, 0, 0)       # transitions 1->2, 2->3 certain; 3->4 loss .2
put("O1_integrated_q", predict_q_exact(c(1, 0)[1:(k - 1)], E, k, M, 1, alpha, beta, .5, 1, 0, 1))
put("O1_frozen_q", predict_q_exact(c(1, 0)[1:(k - 1)], E, k, M, 1, alpha, beta, .5, 1, 0, 1, frozen = TRUE))
put("O1_codex_integrated", .6686076997); put("O1_codex_frozen", .6852245278)

# ---- O2-O4: two genera, five stages, exposure at most 2 -----------------------------------------------------------------
k <- 3; M <- 2; E <- c(2, 1, 2, 1, 2)
alpha <- c(qlogis(.1), qlogis(.15), qlogis(.4), qlogis(.1)); beta <- c(.3, .3, .8, .3)
theta0 <- .4; gw <- .7
prefA <- c(1, 1); prefB <- c(2, 0)
mu0 <- mean(log(c(1, 2))); s0 <- sd(log(c(1, 2)))                     # frozen at the origin from the two prefixes
qA <- predict_q_exact(prefA, E, k, M, 1, alpha, beta, theta0, gw, mu0, s0)
qB <- predict_q_exact(prefB, E, k, M, .7, alpha, beta, theta0, gw, mu0, s0)
# Brute-force joint enumeration over both genera's latent paths (no independence assumed), scaling frozen.
paths <- function(prefix, alive_k1) {          # all (record-in-window indicator, probability) paths for one genus
  out <- list()
  walk <- function(counts, t, alive, pr, inwin) {
    if (t > k + M || !alive) { out[[length(out) + 1]] <<- c(inwin, pr); return(invisible()) }
    phi <- 1 - plogis(alpha[t - 1] + beta[t - 1] * x_tr(counts, t, mu0, s0))
    walk(counts, k + M + 1, FALSE, pr * (1 - phi), inwin)
    r <- 1 - exp(-theta_of(counts, theta0, gw))
    for (cc in 0:E[t]) walk(c(counts, cc), t + 1, TRUE, pr * phi * dbinom(cc, E[t], r), inwin || (t > k && cc > 0))
  }
  out[[1]] <- c(0, 1 - alive_k1)
  walk(prefix, k, TRUE, alive_k1, FALSE)
  do.call(rbind, out)
}
PA <- paths(prefA, 1); PB <- paths(prefB, .7)
put("O2_total_probability_A", sum(PA[, 2])); put("O2_total_probability_B", sum(PB[, 2]))
joint <- outer(PA[, 2], PB[, 2])
lossA <- PA[, 1] == 0; lossB <- PB[, 1] == 0
P11 <- sum(joint[lossA, lossB]); P10 <- sum(joint[lossA, !lossB]); P01 <- sum(joint[!lossA, lossB]); P00 <- sum(joint[!lossA, !lossB])
put("O2_joint_total", P11 + P10 + P01 + P00)
put("O2_marginal_qA_matches_predictor", abs((P11 + P10) - qA))
condD1 <- c(A = P10, B = P01) / (P10 + P01)
put("O2_set_law_D1_normalisation", abs(sum(condD1) - 1))
# Joint recursion over both genera (no independence assumed). frozen = TRUE uses the origin's mu0 and s0;
# frozen = FALSE re-standardises each transition's x over the genera recorded so far (an illustration, not adopted).
joint_enum <- function(frozen) {
  tot <- matrix(0, 2, 2)
  rec <- function(cA, cB, t, aA, aB, pr, wA, wB) {
    if (t > k + M || (!aA && !aB)) { tot[1 + wA, 1 + wB] <<- tot[1 + wA, 1 + wB] + pr; return(invisible()) }
    hA <- cA[seq_len(t - 2)]; hB <- cB[seq_len(t - 2)]
    lastA <- if (any(hA > 0)) log(tail(hA[hA > 0], 1)) else NA; lastB <- if (any(hB > 0)) log(tail(hB[hB > 0], 1)) else NA
    if (frozen) { m <- mu0; sd0 <- s0 } else {
      v <- c(lastA, lastB); m <- mean(v, na.rm = TRUE); sd0 <- if (sum(!is.na(v)) > 1) sd(v, na.rm = TRUE) else 1
      if (!is.finite(sd0) || sd0 == 0) sd0 <- 1
    }
    xA <- if (is.na(lastA)) 0 else (lastA - m) / sd0; xB <- if (is.na(lastB)) 0 else (lastB - m) / sd0
    phA <- if (aA) 1 - plogis(alpha[t - 1] + beta[t - 1] * xA) else 0; phB <- if (aB) 1 - plogis(alpha[t - 1] + beta[t - 1] * xB) else 0
    rA <- 1 - exp(-theta_of(cA, theta0, gw)); rB <- 1 - exp(-theta_of(cB, theta0, gw))
    for (sA in c(TRUE, FALSE)) for (sB in c(TRUE, FALSE)) {
      ps <- (if (sA) phA else 1 - phA) * (if (sB) phB else 1 - phB)
      if (ps == 0) next
      for (ca in (if (sA) 0:E[t] else 0)) for (cb in (if (sB) 0:E[t] else 0)) {
        pc <- (if (sA) dbinom(ca, E[t], rA) else 1) * (if (sB) dbinom(cb, E[t], rB) else 1)
        rec(c(cA, ca), c(cB, cb), t + 1, sA, sB, pr * ps * pc, wA || (t > k && ca > 0), wB || (t > k && cb > 0))
      }
    }
  }
  # membership at k-1: A alive (1), B alive with probability .7
  rec(prefA, prefB, k, TRUE, TRUE, .7, FALSE, FALSE)
  rec(prefA, prefB, k, TRUE, FALSE, .3, FALSE, FALSE)
  tot
}
Jf <- joint_enum(TRUE); Jr <- joint_enum(FALSE)
put("O3_joint_total_frozen", sum(Jf))
put("O3_factorisation_error_frozen_scaling", max(abs(c(Jf[1, 1] - qA * qB, Jf[1, 2] - qA * (1 - qB), Jf[2, 1] - (1 - qA) * qB))))
put("O3_joint_total_restandardised", sum(Jr))
qAr <- Jr[1, 1] + Jr[1, 2]; qBr <- Jr[1, 1] + Jr[2, 1]
put("O3_factorisation_error_restandardised", abs(Jr[1, 1] - qAr * qBr))

# O4: the predictive takes only the prefix; any realised future record pattern leaves it unchanged by construction.
futures <- expand.grid(0:2, 0:1, 0:2)
vals <- apply(futures, 1, function(z) { full <- c(prefA, z); predict_q_exact(full[1:(k - 1)], E, k, M, 1, alpha, beta, theta0, gw, mu0, s0) })
put("O4_futures_enumerated", nrow(futures)); put("O4_predictive_range_over_futures", diff(range(vals)))

# ---- O5: Monte Carlo integration for realistic exposure ---------------------------------------------------------------
predict_q_mc <- function(prefix, E, k, M, alive_k1, alpha, beta, theta0, gw, mu0, s0, n, seed) {
  set.seed(seed); hit <- 0
  for (s in seq_len(n)) {
    counts <- prefix; alive <- runif(1) < alive_k1; inwin <- FALSE; t <- k
    while (alive && t <= k + M) {
      phi <- 1 - plogis(alpha[t - 1] + beta[t - 1] * x_tr(counts, t, mu0, s0))
      if (runif(1) >= phi) { alive <- FALSE; break }
      cc <- rbinom(1, E[t], 1 - exp(-theta_of(counts, theta0, gw)))
      if (t > k && cc > 0) inwin <- TRUE
      counts <- c(counts, cc); t <- t + 1
    }
    hit <- hit + !inwin
  }
  c(q = hit / n, se = sqrt((hit / n) * (1 - hit / n) / n))
}
mc <- predict_q_mc(prefA, E, k, M, 1, alpha, beta, theta0, gw, mu0, s0, 2e5, 38)
put("O5_exact_qA", qA); put("O5_mc_qA", mc[["q"]]); put("O5_mc_se", mc[["se"]]); put("O5_abs_z", abs(mc[["q"]] - qA) / mc[["se"]])

# ---- O6: entry and first capture --------------------------------------------------------------------------------------
# A genus enters (is alive) at stage e with no record yet; theta = theta0 before any record. The first record is the
# first positive count; the count at first capture is zero-truncated Binomial(E_f, r0). With epsilon < 1 the stage of
# death has exposure epsilon * theta, so a first capture tilts survival out of f:
#   P(z_{f+1} = 1 | captured at f) = phi_f p_f / (phi_f p_f + (1 - phi_f) p_f^eps), p = 1 - (1 - r)^E.
Ef <- 2; r0 <- 1 - exp(-theta0); phi_f <- .7
for (eps in c(1, .5)) {
  pe <- 1 - (1 - (1 - exp(-eps * theta0)))^Ef; p <- 1 - (1 - r0)^Ef
  put(sprintf("O6_eps%.1f_tilted_survival_after_first_capture", eps), phi_f * p / (phi_f * p + (1 - phi_f) * pe))
  # enumeration of the generator: survive or die in f, count in f, condition on count > 0
  num <- phi_f * sum(dbinom(1:Ef, Ef, r0)); den <- num + (1 - phi_f) * sum(dbinom(1:Ef, Ef, 1 - exp(-eps * theta0)))
  put(sprintf("O6_eps%.1f_enumerated", eps), num / den)
  put(sprintf("O6_eps%.1f_first_count_is_2_given_capture_and_survival", eps), dbinom(2, Ef, r0) / sum(dbinom(1:Ef, Ef, r0)))
}

# ---- O7: epsilon = .5 masking cut -------------------------------------------------------------------------------------
# Stage-k emission for a genus alive at k depends on the held-out transition when eps < 1 (Codex's numbers, p = .6).
emis <- function(phik, p, eps) phik * p + (1 - phik) * (1 - (1 - p)^eps)
put("O7_stage_k_emission_phi.2", emis(.2, .6, .5)); put("O7_stage_k_emission_phi.9", emis(.9, .6, .5))
# A left component cut at k keeps that emission; cut at k-1 it contains no stage-k term, so it cannot depend on phi_k.
# Enumerated check on a 5-stage history (record at k), eps = .5, varying phi_k: likelihood of stages f..C.
lik_eps_cut <- function(y, f, C, phi, p, eps) {          # P(y_{f+1..C} | first record at f), censored after C
  pe <- 1 - (1 - p)^eps; tot <- 0
  for (d in f:(C + 1)) {                                   # last stage alive (C + 1 = alive beyond C)
    pr <- if (d <= C) prod(phi[f:d][-length(f:d)]) * (1 - phi[d]) else prod(phi[f:C])
    em <- if (d == f) pe[f] else p[f]                      # the first record itself (fixed: Codex 76/2195)
    for (t in (f + 1):C) if (t <= C && t > f) {
      alive <- t <= d; pt <- if (!alive) 0 else if (t == d) pe[t] else p[t]
      em <- em * (if (y[t] == 1) pt else 1 - pt)
    }
    tot <- tot + pr * em
  }
  pf <- phi[f] * p[f] + (1 - phi[f]) * pe[f]
  tot / pf
}
y <- c(1, 0, 1, 0, 1); pp <- c(.6, .5, .6, .5, .6); kk <- 3
ph <- function(e) { v <- c(.8, .8, .8, .8); v[kk] <- e; v }
put("O7_cut_at_k_range_over_phi_k", diff(range(sapply(c(.2, .5, .9), function(e) lik_eps_cut(y, 1, kk, ph(e), pp, .5)))))
put("O7_cut_at_k_minus_1_range_over_phi_k", diff(range(sapply(c(.2, .5, .9), function(e) lik_eps_cut(y, 1, kk - 1, ph(e), pp, .5)))))
put("O7_eps1_cut_at_k_range_over_phi_k", diff(range(sapply(c(.2, .5, .9), function(e) lik_eps_cut(y, 1, kk, ph(e), pp, 1)))))
# Total probability over every continuation of the first record must be 1 (the omitted first emission broke this).
Hs <- as.matrix(expand.grid(rep(list(0:1), kk - 1)))
for (eps in c(1, .5)) put(sprintf("O7_eps%.1f_total_probability_cut_at_k", eps),
                          sum(apply(Hs, 1, function(z) lik_eps_cut(c(1, z, 0, 0), 1, kk, ph(.5), pp, eps))))
# O6b: with counts retained, survival out of the first-capture stage conditions on the actual first count c.
for (cc in 1:Ef) put(sprintf("O6b_eps0.5_survival_given_first_count_%d", cc),
                     phi_f * dbinom(cc, Ef, r0) / (phi_f * dbinom(cc, Ef, r0) + (1 - phi_f) * dbinom(cc, Ef, 1 - exp(-.5 * theta0))))

kv <- data.frame(name = names(res), value = vapply(res, function(v) format(signif(v, 10)), ""))
write.table(kv, file.path(out, "marked_history_oracle.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(kv, row.names = FALSE)

// Q-012 full working likelihood, v4 (Codex 76/1745): as v3, but each cohort mode is found by
// solve_powell_tol, whose evaluation-limit and residual failures are domain errors (rejections),
// not the fatal runtime error KINSOL raises for a failed line search. Explicit guards run in
// order: finite inputs, derived variances and initial score; then the returned mode and score;
// then the residual; then the precision; then the Newton correction; then the factorisation.
// Each failure rejects the proposal with a labelled message. The 2-D covariance factor is the
// closed-form Cholesky factor of the inverse 2x2 precision (algebraically the same quantity as
// v3's cholesky_decompose(inverse_spd(P))). The 40-node adaptive Gauss-Hermite rule is unchanged.
functions {
  int bad(real x) {
    return is_nan(x) || is_inf(x);
  }
  vector score1(vector y, real sig, real A, real B, real kb) {
    real s2h = 0.5 * square(sig);
    return [-y[1] / square(sig) - A * exp(y[1] - s2h) - kb * B * exp(kb * (y[1] - s2h))]';
  }
  vector score2(vector y, real sig, real rho, real Ap, real Bp, real Ad, real Bd, real kb) {
    real s2h = 0.5 * square(sig);
    real sc2 = square(sig) * (1 - square(rho));
    return [-y[1] / square(sig) + rho * (y[2] - rho * y[1]) / sc2 - Ap * exp(y[1] - s2h) - kb * Bp * exp(kb * (y[1] - s2h)),
            -(y[2] - rho * y[1]) / sc2 - Ad * exp(y[2] - s2h) - kb * Bd * exp(kb * (y[2] - s2h))]';
  }
  real logS(real x, real s2h, real A, real B, real kb) {
    return -A * exp(x - s2h) - B * exp(kb * (x - s2h));
  }
  real log_pi_1d(real sig, real A, real B, real kb, vector t, vector w,
                 data real rel_tol, data real f_tol, int max_steps, data real check_tol) {
    int Q = num_elements(t);
    real s2h = 0.5 * square(sig);
    vector[1] y0 = rep_vector(0.0, 1);
    vector[1] my;
    vector[1] g;
    real m;
    real prec;
    real delta;
    real s;
    vector[Q] terms;
    if (bad(sig) || sig <= 0 || bad(square(sig)) || square(sig) <= 0 || bad(s2h) || bad(A) || A < 0
        || bad(B) || B < 0 || bad(kb))
      reject("Q012 input failure: 1-D sigma, A, B, kappa_b ", [sig, A, B, kb]);
    if (bad(score1(y0, sig, A, B, kb)[1]))
      reject("Q012 input failure: 1-D initial score");
    my = solve_powell_tol(score1, y0, rel_tol, f_tol, max_steps, sig, A, B, kb);
    g = score1(my, sig, A, B, kb);
    m = my[1];
    if (bad(m) || bad(g[1]))
      reject("Q012 solver failure: non-finite 1-D mode or score");
    if (abs(g[1]) > check_tol)
      reject("Q012 solver failure: 1-D score residual ", abs(g[1]));
    prec = 1 / square(sig) + A * exp(m - s2h) + square(kb) * B * exp(kb * (m - s2h));
    if (bad(prec) || prec <= 0)
      reject("Q012 Hessian failure: 1-D precision ", prec);
    delta = g[1] / prec;
    if (bad(delta) || abs(delta) > check_tol * fmax(1, abs(m)))
      reject("Q012 solver failure: 1-D Newton correction ", delta);
    s = 1 / sqrt(prec);
    if (bad(s) || s <= 0)
      reject("Q012 factorisation failure: 1-D scale ", s);
    for (q in 1:Q) {
      real x = m + sqrt2() * s * t[q];
      terms[q] = log(w[q]) + square(t[q]) - square(x) / (2 * square(sig)) - log(sig)
                 - 0.5 * log(2 * pi()) + logS(x, s2h, A, B, kb);
    }
    return log(sqrt2() * s) + log_sum_exp(terms);
  }
  real log_pi_2d(real sig, real rho, real Ap, real Bp, real Ad, real Bd, real kb, vector t, vector w,
                 data real rel_tol, data real f_tol, int max_steps, data real check_tol) {
    int Q = num_elements(t);
    real s2h = 0.5 * square(sig);
    real sc2 = square(sig) * (1 - square(rho));
    vector[2] y0 = rep_vector(0.0, 2);
    vector[2] g0;
    vector[2] y;
    vector[2] g;
    matrix[2, 2] P;
    real detP;
    vector[2] delta;
    real L11;
    real L21;
    real L22;
    vector[Q * Q] terms;
    if (bad(sig) || sig <= 0 || bad(square(sig)) || square(sig) <= 0 || bad(s2h) || bad(rho) || rho < 0 || rho >= 1
        || bad(sc2) || sc2 <= 0 || bad(Ap) || Ap < 0 || bad(Bp) || Bp < 0 || bad(Ad) || Ad < 0 || bad(Bd) || Bd < 0
        || bad(kb))
      reject("Q012 input failure: 2-D sigma, rho, conditional variance, A, B, kappa_b ", [sig, rho, sc2, Ap, Bp, Ad, Bd, kb]);
    g0 = score2(y0, sig, rho, Ap, Bp, Ad, Bd, kb);
    if (bad(g0[1]) || bad(g0[2]))
      reject("Q012 input failure: 2-D initial score");
    y = solve_powell_tol(score2, y0, rel_tol, f_tol, max_steps, sig, rho, Ap, Bp, Ad, Bd, kb);
    g = score2(y, sig, rho, Ap, Bp, Ad, Bd, kb);
    if (bad(y[1]) || bad(y[2]) || bad(g[1]) || bad(g[2]))
      reject("Q012 solver failure: non-finite 2-D mode or score");
    if (max(abs(g)) > check_tol)
      reject("Q012 solver failure: 2-D score residual ", max(abs(g)));
    P = [[1 / square(sig) + square(rho) / sc2 + Ap * exp(y[1] - s2h) + square(kb) * Bp * exp(kb * (y[1] - s2h)), -rho / sc2],
         [-rho / sc2, 1 / sc2 + Ad * exp(y[2] - s2h) + square(kb) * Bd * exp(kb * (y[2] - s2h))]];
    detP = P[1, 1] * P[2, 2] - square(P[1, 2]);
    if (bad(P[1, 1]) || bad(P[1, 2]) || bad(P[2, 2]) || bad(detP) || detP <= 0 || P[1, 1] <= 0 || P[2, 2] <= 0)
      reject("Q012 Hessian failure: 2-D precision ", [P[1, 1], P[1, 2], P[2, 2], detP]);
    delta = [P[2, 2] * g[1] - P[1, 2] * g[2], P[1, 1] * g[2] - P[1, 2] * g[1]]' / detP;
    if (bad(delta[1]) || bad(delta[2]) || max(abs(delta)) > check_tol * fmax(1, max(abs(y))))
      reject("Q012 solver failure: 2-D Newton correction ", max(abs(delta)));
    // Cholesky factor of inverse(P): L11 = sqrt(P22 / det), L21 = -P12 / (det * L11), L22 = 1 / sqrt(P22).
    L11 = sqrt(P[2, 2] / detP);
    L21 = -P[1, 2] / (detP * L11);
    L22 = 1 / sqrt(P[2, 2]);
    if (bad(L11) || bad(L21) || bad(L22) || L11 <= 0 || L22 <= 0)
      reject("Q012 factorisation failure: 2-D covariance factor ", [L11, L21, L22]);
    for (q in 1:Q) {
      for (qq in 1:Q) {
        real x1 = y[1] + sqrt2() * L11 * t[q];
        real x2 = y[2] + sqrt2() * (L21 * t[q] + L22 * t[qq]);
        terms[(q - 1) * Q + qq] = log(w[q]) + log(w[qq]) + square(t[q]) + square(t[qq])
                                  - square(x1) / (2 * square(sig)) - log(sig)
                                  - square(x2 - rho * x1) / (2 * sc2) - 0.5 * log(sc2) - log(2 * pi())
                                  + logS(x1, s2h, Ap, Bp, kb) + logS(x2, s2h, Ad, Bd, kb);
      }
    }
    return log(2.0) + log(L11 * L22) + log_sum_exp(terms);
  }
}
data {
  int<lower=1> N;
  array[N] int<lower=0> parent;
  vector[N] o;
  vector[N] v;
  vector[N] r;
  array[N] int<lower=0, upper=1> ext;
  array[N] int<lower=0, upper=1> bif;
  vector[N] mplus;
  int<lower=1> S;
  array[N] int<lower=1> seg_start;     // first segment of lineage i (segments contiguous per lineage)
  array[N] int<lower=1> seg_len;
  array[S] int<lower=1, upper=25> seg_bin;
  vector[S] seg_a0;
  vector[S] seg_a1;
  vector[S] seg_E;
  vector[S] seg_miss;
  array[N] int<lower=1, upper=25> term_bin;
  vector[N] term_a;
  vector[N] term_E;
  vector[N] term_miss;
  int<lower=0> SP;
  array[SP] int<lower=1, upper=N> pre_lin;
  array[SP] int<lower=1, upper=25> pre_bin;
  vector[SP] pre_a0;
  vector[SP] pre_a1;
  real c;
  int<lower=0> NC;
  array[NC] int<lower=1, upper=N> coh;
  int<lower=0> C1;
  array[C1] int<lower=1, upper=N> c1_lin;
  int<lower=0> C2;
  array[C2] int<lower=1, upper=N> c2_par;
  array[C2] int<lower=1, upper=N> c2_dau;
  int<lower=1> Q;
  vector[Q] gh_t;
  vector[Q] gh_w;
  real<lower=0> solver_rel_tol;            // Powell relative solution tolerance
  real<lower=0> solver_f_tol;              // Powell Euclidean residual tolerance
  int<lower=1> solver_max_steps;           // Powell maximum function evaluations
  real<lower=0> check_tol;            // Codex's post-solve threshold, fixed at 1e-8
}
transformed data {
  vector[N] dpost = v - r;
  vector[N] extv = to_vector(ext);
  vector[N] bifv = to_vector(bif);
  vector[N] log_term_a = log(term_a);
}
parameters {
  real log_h0_1;
  vector[24] z_rw;
  real<lower=0> tau;
  real log_k;
  real log_lambda0;
  real kappa;
  real log_b0;
  real kappa_b;
  real beta;
  real gamma;
  real<lower=0> sigma;
  real<lower=0, upper=1> rho;
  vector[N] eps;
}
transformed parameters {
  vector[25] log_h0;
  vector[N] x;
  log_h0[1] = log_h0_1;
  for (j in 2:25)
    log_h0[j] = log_h0[j - 1] + tau * z_rw[j - 1];
  for (i in 1:N) {
    if (parent[i] == 0)
      x[i] = sigma * eps[i];
    else
      x[i] = rho * x[parent[i]] + sigma * sqrt(1 - square(rho)) * eps[i];
  }
}
model {
  real k = exp(log_k);
  real lambda0 = exp(log_lambda0);
  real b0 = exp(log_b0);
  vector[N] logz = x - 0.5 * square(sigma);
  vector[S] segval = exp(log_h0[seg_bin] + beta * seg_E + gamma * seg_miss) .* (pow(seg_a1, k) - pow(seg_a0, k));
  vector[N] cum;
  vector[N] A = rep_vector(0, N);
  log_h0_1 ~ normal(log(0.065), 1);
  z_rw ~ std_normal();
  tau ~ normal(0, 0.5);
  log_k ~ normal(0, 0.5);
  log_lambda0 ~ normal(log(0.0708), 1);
  kappa ~ normal(0, 1);
  log_b0 ~ normal(log(0.0082), 1);
  kappa_b ~ normal(0, 1);
  beta ~ normal(0, 1);
  gamma ~ normal(0, 1);
  sigma ~ normal(0, 1);
  eps ~ std_normal();
  for (i in 1:N)
    cum[i] = sum(segment(segval, seg_start[i], seg_len[i]));
  target += -dot_product(exp(logz), cum) - b0 * dot_product(exp(kappa_b * logz), dpost);
  target += dot_product(extv, logz + log_h0[term_bin] + log_k + (k - 1) * log_term_a + beta * term_E + gamma * term_miss);
  target += dot_product(bifv, log_b0 + kappa_b * logz);
  target += dot_product(mplus, log_lambda0 + kappa * logz) - lambda0 * dot_product(exp(kappa * logz), dpost);
  if (NC > 0) {
    for (s in 1:SP)
      A[pre_lin[s]] += exp(log_h0[pre_bin[s]] + gamma) * (pow(pre_a1[s], k) - pow(pre_a0[s], k));
    for (j in 1:NC) {
      int i = coh[j];
      target += logS(x[i], 0.5 * square(sigma), A[i], b0 * (c - o[i]), kappa_b);
    }
    for (j in 1:C1) {
      int i = c1_lin[j];
      target += -log_pi_1d(sigma, A[i], b0 * (c - o[i]), kappa_b, gh_t, gh_w,
                           solver_rel_tol, solver_f_tol, solver_max_steps, check_tol);
    }
    for (j in 1:C2)
      target += -log_pi_2d(sigma, rho, A[c2_par[j]], b0 * (c - o[c2_par[j]]),
                           A[c2_dau[j]], b0 * (c - o[c2_dau[j]]), kappa_b, gh_t, gh_w,
                           solver_rel_tol, solver_f_tol, solver_max_steps, check_tol);
  }
}
generated quantities {
  real eta = rho * sigma;
}

// Q-012 full working likelihood, v3 (Codex 76/1742): as v2, but each cohort mode is found by
// Stan's solve_newton_tol (KINSOL line search, implicit derivatives), with explicit post-solve
// checks; the 40-node adaptive Gauss-Hermite rule is unchanged so the solver change is isolated.
functions {
  // Score (gradient) of the concave log integrand for one cohort lineage, and for a pair.
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
  // Explicit post-solve checks (Codex 76/1742): finite values, score infinity norm, and a
  // curvature-scaled Newton correction. Failures reject the proposal with a labelled message.
  void check_mode(vector m, vector g, vector delta, real ftol) {
    for (j in 1:num_elements(m))
      if (is_nan(m[j]) || is_inf(m[j]) || is_nan(g[j]) || is_inf(g[j]))
        reject("Q012 solver failure: non-finite mode or score");
    if (max(abs(g)) > ftol)
      reject("Q012 solver failure: score residual ", max(abs(g)));
    if (max(abs(delta)) > ftol * fmax(1, max(abs(m))))
      reject("Q012 solver failure: Newton correction ", max(abs(delta)));
  }
  real log_pi_1d(real sig, real A, real B, real kb, vector t, vector w,
                 data real step_tol, data real f_tol, int max_steps, data real check_tol) {
    int Q = num_elements(t);
    real s2h = 0.5 * square(sig);
    vector[1] my = solve_newton_tol(score1, rep_vector(0.0, 1), step_tol, f_tol, max_steps, sig, A, B, kb);
    real m = my[1];
    real prec = 1 / square(sig) + A * exp(m - s2h) + square(kb) * B * exp(kb * (m - s2h));
    vector[1] g = score1(my, sig, A, B, kb);
    real s;
    vector[Q] terms;
    if (is_nan(prec) || is_inf(prec) || prec <= 0)
      reject("Q012 Hessian failure: 1-D precision ", prec);
    check_mode(my, g, g / prec, check_tol);
    s = 1 / sqrt(prec);
    for (q in 1:Q) {
      real x = m + sqrt2() * s * t[q];
      terms[q] = log(w[q]) + square(t[q]) - square(x) / (2 * square(sig)) - log(sig)
                 - 0.5 * log(2 * pi()) + logS(x, s2h, A, B, kb);
    }
    return log(sqrt2() * s) + log_sum_exp(terms);
  }
  real log_pi_2d(real sig, real rho, real Ap, real Bp, real Ad, real Bd, real kb, vector t, vector w,
                 data real step_tol, data real f_tol, int max_steps, data real check_tol) {
    int Q = num_elements(t);
    real s2h = 0.5 * square(sig);
    real sc2 = square(sig) * (1 - square(rho));
    vector[2] y = solve_newton_tol(score2, rep_vector(0.0, 2), step_tol, f_tol, max_steps, sig, rho, Ap, Bp, Ad, Bd, kb);
    vector[2] g = score2(y, sig, rho, Ap, Bp, Ad, Bd, kb);
    matrix[2, 2] P = [[1 / square(sig) + square(rho) / sc2 + Ap * exp(y[1] - s2h) + square(kb) * Bp * exp(kb * (y[1] - s2h)), -rho / sc2],
                      [-rho / sc2, 1 / sc2 + Ad * exp(y[2] - s2h) + square(kb) * Bd * exp(kb * (y[2] - s2h))]];
    real detP = P[1, 1] * P[2, 2] - P[1, 2] * P[2, 1];
    matrix[2, 2] Lc;
    vector[Q * Q] terms;
    if (is_nan(detP) || is_inf(detP) || detP <= 0 || P[1, 1] <= 0)
      reject("Q012 Hessian failure: 2-D precision determinant ", detP);
    check_mode(y, g, mdivide_left(P, g), check_tol);
    Lc = cholesky_decompose(inverse_spd(P));
    for (j in 1:2)
      if (is_nan(Lc[j, j]) || is_inf(Lc[j, j]) || Lc[j, j] <= 0)
        reject("Q012 Hessian failure: Cholesky factor");
    for (q in 1:Q) {
      for (qq in 1:Q) {
        real x1 = y[1] + sqrt2() * Lc[1, 1] * t[q];
        real x2 = y[2] + sqrt2() * (Lc[2, 1] * t[q] + Lc[2, 2] * t[qq]);
        terms[(q - 1) * Q + qq] = log(w[q]) + log(w[qq]) + square(t[q]) + square(t[qq])
                                  - square(x1) / (2 * square(sig)) - log(sig)
                                  - square(x2 - rho * x1) / (2 * sc2) - 0.5 * log(sc2) - log(2 * pi())
                                  + logS(x1, s2h, Ap, Bp, kb) + logS(x2, s2h, Ad, Bd, kb);
      }
    }
    return log(2.0) + log(Lc[1, 1] * Lc[2, 2]) + log_sum_exp(terms);
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
  real<lower=0> solver_step_tol;
  real<lower=0> solver_f_tol;
  int<lower=1> solver_max_steps;
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
                           solver_step_tol, solver_f_tol, solver_max_steps, check_tol);
    }
    for (j in 1:C2)
      target += -log_pi_2d(sigma, rho, A[c2_par[j]], b0 * (c - o[c2_par[j]]),
                           A[c2_dau[j]], b0 * (c - o[c2_dau[j]]), kappa_b, gh_t, gh_w,
                           solver_step_tol, solver_f_tol, solver_max_steps, check_tol);
  }
}
generated quantities {
  real eta = rho * sigma;
}

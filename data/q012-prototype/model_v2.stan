// Q-012 full working likelihood, v2 (after Codex 76/1737).
// Changes from model.stan (v1, preserved): (1) the cohort normaliser uses adaptive
// Gauss-Hermite quadrature centred at the (jointly concave) integrand's mode, 1-D or 2-D;
// (2) the baseline random walk is non-centred, which leaves the joint prior of log_h0
// unchanged; (3) the segment hazard sum is vectorised over contiguous per-lineage blocks.
functions {
  real logS(real x, real s2h, real A, real B, real kb) {
    return -A * exp(x - s2h) - B * exp(kb * (x - s2h));
  }
  real log_pi_1d(real sig, real A, real B, real kb, vector t, vector w) {
    int Q = num_elements(t);
    real s2h = 0.5 * square(sig);
    real m = 0;
    real s;
    vector[Q] terms;
    for (it in 1:50) {
      real e1 = A * exp(m - s2h);
      real e2 = B * exp(kb * (m - s2h));
      m -= (-m / square(sig) - e1 - kb * e2) / (-1 / square(sig) - e1 - square(kb) * e2);
    }
    s = 1 / sqrt(1 / square(sig) + A * exp(m - s2h) + square(kb) * B * exp(kb * (m - s2h)));
    for (q in 1:Q) {
      real x = m + sqrt2() * s * t[q];
      terms[q] = log(w[q]) + square(t[q]) - square(x) / (2 * square(sig)) - log(sig)
                 - 0.5 * log(2 * pi()) + logS(x, s2h, A, B, kb);
    }
    return log(sqrt2() * s) + log_sum_exp(terms);
  }
  real log_pi_2d(real sig, real rho, real Ap, real Bp, real Ad, real Bd, real kb, vector t, vector w) {
    int Q = num_elements(t);
    real s2h = 0.5 * square(sig);
    real sc2 = square(sig) * (1 - square(rho));
    vector[2] y = rep_vector(0, 2);
    matrix[2, 2] P;
    matrix[2, 2] Lc;
    vector[Q * Q] terms;
    for (it in 1:50) {
      real ep1 = Ap * exp(y[1] - s2h);
      real ep2 = Bp * exp(kb * (y[1] - s2h));
      real ed1 = Ad * exp(y[2] - s2h);
      real ed2 = Bd * exp(kb * (y[2] - s2h));
      vector[2] g = [-y[1] / square(sig) + rho * (y[2] - rho * y[1]) / sc2 - ep1 - kb * ep2,
                     -(y[2] - rho * y[1]) / sc2 - ed1 - kb * ed2]';
      matrix[2, 2] H = [[-1 / square(sig) - square(rho) / sc2 - ep1 - square(kb) * ep2, rho / sc2],
                        [rho / sc2, -1 / sc2 - ed1 - square(kb) * ed2]];
      y = y - mdivide_left(H, g);
    }
    P = -[[-1 / square(sig) - square(rho) / sc2 - Ap * exp(y[1] - s2h) - square(kb) * Bp * exp(kb * (y[1] - s2h)), rho / sc2],
          [rho / sc2, -1 / sc2 - Ad * exp(y[2] - s2h) - square(kb) * Bd * exp(kb * (y[2] - s2h))]];
    Lc = cholesky_decompose(inverse_spd(P));
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
      target += -log_pi_1d(sigma, A[i], b0 * (c - o[i]), kappa_b, gh_t, gh_w);
    }
    for (j in 1:C2)
      target += -log_pi_2d(sigma, rho, A[c2_par[j]], b0 * (c - o[c2_par[j]]),
                           A[c2_dau[j]], b0 * (c - o[c2_dau[j]]), kappa_b, gh_t, gh_w);
  }
}
generated quantities {
  real eta = rho * sigma;
}

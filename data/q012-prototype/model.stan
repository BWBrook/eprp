// Q-012 full working likelihood (finite contract, Amendment 1), complete-ascertainment
// working model. Forward time u = 75 - t_Ma; boundary c. Lineages ordered parents first.
// Post-entry hazard terms use segments split at 1-Myr exposure bins and 3-Myr baseline
// bins; ages a = u - o are never reset at entry. Cohort lineages (origin before c) add
// termination survival from origin to c, and the likelihood is divided by the cohort
// normaliser, computed per connected component by Gauss-Hermite quadrature.
functions {
  // log S(c | x) for a cohort lineage: pre-entry termination survival
  real log_surv_pre(real x, real sigma, real A, real b0, real kappa_b, real dpre) {
    real logz = x - 0.5 * square(sigma);
    return -exp(logz) * A - b0 * exp(kappa_b * logz) * dpre;
  }
}
data {
  int<lower=1> N;
  array[N] int<lower=0> parent;
  vector[N] o;
  vector[N] v;
  vector[N] r;                         // entry: max(o, c) for cohort lineages, else o
  array[N] int<lower=0, upper=1> ext;  // terminal extinction
  array[N] int<lower=0, upper=1> bif;  // terminal bifurcation candidate
  array[N] int<lower=0> mplus;         // recorded buds after entry
  int<lower=1> S;                      // post-entry segments
  array[S] int<lower=1, upper=N> seg_lin;
  array[S] int<lower=1, upper=25> seg_bin;
  vector[S] seg_a0;
  vector[S] seg_a1;
  vector[S] seg_E;
  vector[S] seg_miss;
  array[N] int<lower=1, upper=25> term_bin;
  vector[N] term_a;
  vector[N] term_E;
  vector[N] term_miss;
  int<lower=0> SP;                     // pre-entry segments (cohort only; exposure missing)
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
}
parameters {
  vector[25] log_h0;
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
  vector[N] x;
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
  vector[N] cum = rep_vector(0, N);
  vector[N] A = rep_vector(0, N);
  // priors
  log_h0[1] ~ normal(log(0.065), 1);
  log_h0[2:25] - log_h0[1:24] ~ normal(0, tau);
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
  // post-entry cumulative extinction hazard (without z)
  for (s in 1:S)
    cum[seg_lin[s]] += exp(log_h0[seg_bin[s]] + beta * seg_E[s] + gamma * seg_miss[s])
                       * (pow(seg_a1[s], k) - pow(seg_a0[s], k));
  for (i in 1:N) {
    target += -exp(logz[i]) * cum[i] - b0 * exp(kappa_b * logz[i]) * dpost[i];
    if (ext[i] == 1)
      target += logz[i] + log_h0[term_bin[i]] + log_k + (k - 1) * log(term_a[i])
                + beta * term_E[i] + gamma * term_miss[i];
    if (bif[i] == 1)
      target += log_b0 + kappa_b * logz[i];
    target += mplus[i] * (log_lambda0 + kappa * logz[i]) - lambda0 * exp(kappa * logz[i]) * dpost[i];
  }
  // cohort: pre-entry survival for the tree's own frailties, divided by the normaliser
  if (NC > 0) {
    for (s in 1:SP)
      A[pre_lin[s]] += exp(log_h0[pre_bin[s]] + gamma) * (pow(pre_a1[s], k) - pow(pre_a0[s], k));
    for (j in 1:NC) {
      int i = coh[j];
      target += log_surv_pre(x[i], sigma, A[i], b0, kappa_b, c - o[i]);
    }
    for (j in 1:C1) {
      int i = c1_lin[j];
      vector[Q] terms;
      for (q in 1:Q)
        terms[q] = log(gh_w[q]) - 0.5 * log(pi())
                   + log_surv_pre(sqrt2() * sigma * gh_t[q], sigma, A[i], b0, kappa_b, c - o[i]);
      target += -log_sum_exp(terms);
    }
    for (j in 1:C2) {
      int ip = c2_par[j];
      int id = c2_dau[j];
      vector[Q * Q] terms;
      for (q in 1:Q) {
        real xp = sqrt2() * sigma * gh_t[q];
        real lp = log_surv_pre(xp, sigma, A[ip], b0, kappa_b, c - o[ip]);
        for (qq in 1:Q) {
          real xd = rho * xp + sqrt2() * sigma * sqrt(1 - square(rho)) * gh_t[qq];
          terms[(q - 1) * Q + qq] = log(gh_w[q]) + log(gh_w[qq]) - log(pi()) + lp
                                    + log_surv_pre(xd, sigma, A[id], b0, kappa_b, c - o[id]);
        }
      }
      target += -log_sum_exp(terms);
    }
  }
}
generated quantities {
  real eta = rho * sigma;
}

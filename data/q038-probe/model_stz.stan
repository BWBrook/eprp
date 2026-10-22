// Q-038 DIAGNOSTIC variant of model.stan (not adopted): family, order, detection-family and detection-stage effects are
// sum-to-zero within class, so intercepts carry their means (pilot divergence diagnosis, README). Likelihood unchanged.
functions {
  real partial_ll(array[] int idx, int start, int end,
                  array[] int c_cls, array[] int c_fam, array[] int c_ord, array[] int c_f, array[] int c_C,
                  array[] int c_last, array[] int c_tr0, array[] int c_em0,
                  array[] int tr_s, matrix tr_feat, array[] int em_y, array[] int em_E, vector em_w,
                  matrix alpha, matrix omega, vector beta_b, vector beta_e, vector delta, matrix gam,
                  matrix f_fam, matrix g_ord, vector gd0, vector gd, matrix b_fam, matrix nu,
                  array[] int ev_of) {
    real lp = 0;
    for (n in 1:(end - start + 1)) {
      int i = idx[n];
      int cl = c_cls[i];
      int f = c_f[i];
      int C = c_C[i];
      int l = c_last[i];
      int m = C - f;
      if (m == 0) continue;
      vector[m] lphi;
      vector[m] l1mphi;
      vector[m] lp0;
      real ll = 0;
      for (j in 1:m) {
        int s = tr_s[c_tr0[i] + j - 1];
        real x = tr_feat[c_tr0[i] + j - 1, 1];
        real e = alpha[cl, s] + gam[cl, 1] * tr_feat[c_tr0[i] + j - 1, 2] + gam[cl, 2] * tr_feat[c_tr0[i] + j - 1, 3]
                 + gam[cl, 3] * tr_feat[c_tr0[i] + j - 1, 4] + f_fam[cl, c_fam[i]] + g_ord[cl, c_ord[i]];
        int k = ev_of[s];
        if (k > 0)
          e += omega[cl, k] + (beta_e[cl] + delta[k]) * x;
        else
          e += beta_b[cl] * x;
        l1mphi[j] = log_inv_logit(e);
        lphi[j] = log_inv_logit(-e);
        int t = s + 1;
        int r = c_em0[i] + j - 1;
        real th = exp(gd0[cl] + gd[cl] * em_w[r] + b_fam[cl, c_fam[i]] + nu[cl, t]);
        lp0[j] = -th * em_E[r];
        if (t <= l) {
          if (em_y[r] == 0)
            ll += lp0[j];
          else
            ll += lchoose(em_E[r], em_y[r]) + em_y[r] * log1m_exp(-th) - (em_E[r] - em_y[r]) * th;
        }
      }
      if (l > f) ll += sum(lphi[1:(l - f)]);
      real logchi = 0;
      for (jj in 1:(C - l)) {
        int j = C - f - jj + 1;          // transition s = C - jj, index j = s - f + 1
        logchi = log_sum_exp(l1mphi[j], lphi[j] + lp0[j] + logchi);
      }
      lp += ll + logchi;
    }
    return lp;
  }
}
data {
  int<lower=1> T;                         // stages
  int<lower=1> N;                         // components
  array[N] int<lower=1, upper=2> c_cls;
  array[N] int<lower=1> c_fam;
  array[N] int<lower=1> c_ord;
  array[N] int<lower=1> c_f;
  array[N] int<lower=1> c_C;
  array[N] int<lower=1> c_last;           // last recorded stage within [f, C]
  array[N] int<lower=1> c_tr0;            // first transition row (rows s = f..C-1); emission rows aligned (t = s + 1)
  array[N] int<lower=1> c_em0;
  int<lower=0> R;                         // transition / emission rows
  array[R] int<lower=1> tr_s;
  matrix[R, 4] tr_feat;                   // x_occ, recency, age, completeness (fixed transforms)
  array[R] int<lower=0> em_y;
  array[R] int<lower=0> em_E;
  vector[R] em_w;
  int<lower=1> NF;                        // families per class
  int<lower=1> NO;                        // orders per class
  array[T] int<lower=0, upper=5> ev_of;   // event index of transition s (0 = background)
  int<lower=0, upper=1> likelihood_only;  // 1: no priors (exact likelihood checks)
  int<lower=1> grainsize;
}
transformed data {
  array[N] int idx;
  for (i in 1:N) idx[i] = i;
}
parameters {
  vector[2] alpha1;
  matrix[2, T - 1] z_alpha;
  vector<lower=0>[2] s_alpha;
  matrix[2, 5] z_omega;
  real mu_omega;
  real<lower=0> s_omega;
  vector[2] beta_b;
  vector[2] beta_e;
  vector[5] z_delta;
  real<lower=0> tau;
  matrix[2, 3] gam;
  array[2] sum_to_zero_vector[NF] z_fam;
  array[2] sum_to_zero_vector[NO] z_ord;
  real<lower=0> s_fam;
  real<lower=0> s_ord;
  vector[2] gd0;
  vector[2] gd;
  array[2] sum_to_zero_vector[NF] z_b;
  real<lower=0> s_b;
  array[2] sum_to_zero_vector[T] z_nu;
  real<lower=0> s_nu;
}
transformed parameters {
  matrix[2, T] alpha;
  matrix[2, 5] omega = mu_omega + s_omega * z_omega;
  vector[5] delta = tau * z_delta;
  matrix[2, NF] f_fam;
  matrix[2, NO] g_ord;
  matrix[2, NF] b_fam;
  matrix[2, T] nu;
  for (c in 1:2) {
    f_fam[c] = s_fam * z_fam[c]';
    g_ord[c] = s_ord * z_ord[c]';
    b_fam[c] = s_b * z_b[c]';
    nu[c] = s_nu * z_nu[c]';
  }
  for (c in 1:2) {
    alpha[c, 1] = alpha1[c];
    for (s in 2:T) alpha[c, s] = alpha[c, s - 1] + s_alpha[c] * z_alpha[c, s - 1];
  }
}
model {
  if (!likelihood_only) {
    alpha1 ~ normal(logit(0.1), 1.5);
    to_vector(z_alpha) ~ std_normal();
    s_alpha ~ normal(0, 0.5);
    to_vector(z_omega) ~ std_normal();
    mu_omega ~ normal(1, 1);
    s_omega ~ normal(0, 1);
    beta_b ~ normal(0, 1);
    beta_e ~ normal(0, 1);
    z_delta ~ std_normal();
    tau ~ normal(0, 0.5);
    to_vector(gam) ~ normal(0, 1);
    for (c in 1:2) {
      z_fam[c] ~ normal(0, inv_sqrt(1 - inv(NF)));
      z_ord[c] ~ normal(0, inv_sqrt(1 - inv(NO)));
      z_b[c] ~ normal(0, inv_sqrt(1 - inv(NF)));
      z_nu[c] ~ normal(0, inv_sqrt(1 - inv(T)));
    }
    s_fam ~ normal(0, 0.5);
    s_ord ~ normal(0, 0.5);
    gd0 ~ normal(log(0.01), 2);
    gd ~ normal(0, 1);
    s_b ~ normal(0, 0.5);
    s_nu ~ normal(0, 0.5);
  }
  target += reduce_sum(partial_ll, idx, grainsize, c_cls, c_fam, c_ord, c_f, c_C, c_last, c_tr0, c_em0,
                       tr_s, tr_feat, em_y, em_E, em_w, alpha, omega, beta_b, beta_e, delta, gam,
                       f_fam, g_ord, gd0, gd, b_fam, nu, ev_of);
}

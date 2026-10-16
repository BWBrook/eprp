// Q-012 tiny component check: complete-history working likelihood with
// budding and extinction only (no bifurcation, exposure or selection).
// Lineages are ordered so that every parent precedes its daughters.
// Forward time u; o = origin, v = end (extinction or horizon censor).
data {
  int<lower=1> N;
  array[N] int<lower=0> parent;      // 0 for roots
  vector[N] o;
  vector[N] v;
  array[N] int<lower=0, upper=1> ext; // 1 = extinction at v, 0 = censored
  array[N] int<lower=0> m;            // number of buds during (o, v]
}
transformed data {
  vector[N] d = v - o;
}
parameters {
  real log_mu0;
  real log_k;
  real log_lambda0;
  real kappa;
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
  real mu0 = exp(log_mu0);
  real k = exp(log_k);
  real lambda0 = exp(log_lambda0);
  vector[N] logz = x - 0.5 * square(sigma);
  log_mu0 ~ normal(log(0.08), 1);
  log_k ~ normal(0, 0.5);
  log_lambda0 ~ normal(log(0.09), 1);
  kappa ~ normal(0, 1);
  sigma ~ normal(0, 1);
  eps ~ std_normal();
  for (i in 1:N) {
    // extinction: hazard z mu0 k a^(k-1); cumulative z mu0 d^k
    target += -exp(logz[i]) * mu0 * pow(d[i], k);
    if (ext[i] == 1)
      target += logz[i] + log_mu0 + log_k + (k - 1) * log(d[i]);
    // budding: homogeneous Poisson at rate lambda0 z^kappa over (o, v]
    target += m[i] * (log_lambda0 + kappa * logz[i]) - lambda0 * exp(kappa * logz[i]) * d[i];
  }
}
generated quantities {
  real eta = rho * sigma;
}

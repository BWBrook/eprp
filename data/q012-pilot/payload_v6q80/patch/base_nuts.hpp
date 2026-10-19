#ifndef STAN_MCMC_HMC_NUTS_BASE_NUTS_HPP
#define STAN_MCMC_HMC_NUTS_BASE_NUTS_HPP

#include <stan/callbacks/logger.hpp>
#include <stan/math/prim.hpp>
#include <stan/mcmc/hmc/base_hmc.hpp>
#include <stan/mcmc/hmc/hamiltonians/ps_point.hpp>
#include <stan/mcmc/hmc/hamiltonians/dense_e_point.hpp>
#include <stan/mcmc/hmc/hamiltonians/diag_e_point.hpp>
#include <stan/mcmc/hmc/hamiltonians/unit_e_point.hpp>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <limits>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace stan {
namespace mcmc {
/**
 * The No-U-Turn sampler (NUTS) with multinomial sampling
 */
template <class Model, template <class, class> class Hamiltonian,
          template <class> class Integrator, class BaseRNG>
class base_nuts : public base_hmc<Model, Hamiltonian, Integrator, BaseRNG> {
 public:
  base_nuts(const Model& model, BaseRNG& rng)
      : base_hmc<Model, Hamiltonian, Integrator, BaseRNG>(model, rng),
        depth_(0),
        max_depth_(5),
        max_deltaH_(1000),
        n_leapfrog_(0),
        divergent_(false),
        energy_(0) {}

  /**
   * specialized constructor for specified diag mass matrix
   */
  base_nuts(const Model& model, BaseRNG& rng, Eigen::VectorXd& inv_e_metric)
      : base_hmc<Model, Hamiltonian, Integrator, BaseRNG>(model, rng,
                                                          inv_e_metric),
        depth_(0),
        max_depth_(5),
        max_deltaH_(1000),
        n_leapfrog_(0),
        divergent_(false),
        energy_(0) {}

  /**
   * specialized constructor for specified dense mass matrix
   */
  base_nuts(const Model& model, BaseRNG& rng, Eigen::MatrixXd& inv_e_metric)
      : base_hmc<Model, Hamiltonian, Integrator, BaseRNG>(model, rng,
                                                          inv_e_metric),
        depth_(0),
        max_depth_(5),
        max_deltaH_(1000),
        n_leapfrog_(0),
        divergent_(false),
        energy_(0) {}

  ~base_nuts() { q012_finish(); }

  void set_metric(const Eigen::MatrixXd& inv_e_metric) {
    this->z_.set_metric(inv_e_metric);
  }

  void set_metric(const Eigen::VectorXd& inv_e_metric) {
    this->z_.set_metric(inv_e_metric);
  }

  void set_max_depth(int d) {
    if (d > 0)
      max_depth_ = d;
  }

  void set_max_delta(double d) { max_deltaH_ = d; }

  int get_max_depth() { return this->max_depth_; }
  double get_max_delta() { return this->max_deltaH_; }

  sample transition(sample& init_sample, callbacks::logger& logger) {
    if (!q012_ready_)
      q012_setup();
    ++q012_transition_;

    // Initialize the algorithm
    this->sample_stepsize();

    this->seed(init_sample.cont_params());

    this->hamiltonian_.sample_p(this->z_, this->rand_int_);
    this->hamiltonian_.init(this->z_, logger);
    if (q012_on_)
      q012_copy(q012_initial_, this->z_);

    ps_point z_fwd(this->z_);  // State at forward end of trajectory
    ps_point z_bck(z_fwd);     // State at backward end of trajectory

    ps_point z_sample(z_fwd);
    ps_point z_propose(z_fwd);

    // Momentum and sharp momentum at forward end of forward subtree
    Eigen::VectorXd p_fwd_fwd = this->z_.p;
    Eigen::VectorXd p_sharp_fwd_fwd = this->hamiltonian_.dtau_dp(this->z_);

    // Momentum and sharp momentum at backward end of forward subtree
    Eigen::VectorXd p_fwd_bck = this->z_.p;
    Eigen::VectorXd p_sharp_fwd_bck = p_sharp_fwd_fwd;

    // Momentum and sharp momentum at forward end of backward subtree
    Eigen::VectorXd p_bck_fwd = this->z_.p;
    Eigen::VectorXd p_sharp_bck_fwd = p_sharp_fwd_fwd;

    // Momentum and sharp momentum at backward end of backward subtree
    Eigen::VectorXd p_bck_bck = this->z_.p;
    Eigen::VectorXd p_sharp_bck_bck = p_sharp_fwd_fwd;

    // Integrated momenta along trajectory
    Eigen::VectorXd rho = this->z_.p.transpose();

    // Log sum of state weights (offset by H0) along trajectory
    double log_sum_weight = 0;  // log(exp(H0 - H0))
    double H0 = this->hamiltonian_.H(this->z_);
    int n_leapfrog = 0;
    double sum_metro_prob = 0;

    // Build a trajectory until the no-u-turn
    // criterion is no longer satisfied
    this->depth_ = 0;
    this->divergent_ = false;

    while (this->depth_ < this->max_depth_) {
      // Build a new subtree in a random direction
      Eigen::VectorXd rho_fwd = Eigen::VectorXd::Zero(rho.size());
      Eigen::VectorXd rho_bck = Eigen::VectorXd::Zero(rho.size());

      bool valid_subtree = false;
      double log_sum_weight_subtree = -std::numeric_limits<double>::infinity();

      if (this->rand_uniform_() > 0.5) {
        // Extend the current trajectory forward
        this->z_.ps_point::operator=(z_fwd);
        rho_bck = rho;
        p_bck_fwd = p_fwd_fwd;
        p_sharp_bck_fwd = p_sharp_fwd_fwd;

        valid_subtree = build_tree(
            this->depth_, z_propose, p_sharp_fwd_bck, p_sharp_fwd_fwd, rho_fwd,
            p_fwd_bck, p_fwd_fwd, H0, 1, n_leapfrog, log_sum_weight_subtree,
            sum_metro_prob, logger);
        z_fwd.ps_point::operator=(this->z_);
      } else {
        // Extend the current trajectory backwards
        this->z_.ps_point::operator=(z_bck);
        rho_fwd = rho;
        p_fwd_bck = p_bck_bck;
        p_sharp_fwd_bck = p_sharp_bck_bck;

        valid_subtree = build_tree(
            this->depth_, z_propose, p_sharp_bck_fwd, p_sharp_bck_bck, rho_bck,
            p_bck_fwd, p_bck_bck, H0, -1, n_leapfrog, log_sum_weight_subtree,
            sum_metro_prob, logger);
        z_bck.ps_point::operator=(this->z_);
      }

      if (!valid_subtree)
        break;

      // Sample from accepted subtree
      ++(this->depth_);

      if (log_sum_weight_subtree > log_sum_weight) {
        z_sample = z_propose;
      } else {
        double accept_prob = std::exp(log_sum_weight_subtree - log_sum_weight);
        if (this->rand_uniform_() < accept_prob)
          z_sample = z_propose;
      }

      log_sum_weight
          = math::log_sum_exp(log_sum_weight, log_sum_weight_subtree);

      // Break when no-u-turn criterion is no longer satisfied
      rho = rho_bck + rho_fwd;

      // Demand satisfaction around merged subtrees
      bool persist_criterion
          = compute_criterion(p_sharp_bck_bck, p_sharp_fwd_fwd, rho);

      // Demand satisfaction between subtrees
      Eigen::VectorXd rho_extended = rho_bck + p_fwd_bck;

      persist_criterion
          &= compute_criterion(p_sharp_bck_bck, p_sharp_fwd_bck, rho_extended);

      rho_extended = rho_fwd + p_bck_fwd;
      persist_criterion
          &= compute_criterion(p_sharp_bck_fwd, p_sharp_fwd_fwd, rho_extended);

      if (!persist_criterion)
        break;
    }

    this->n_leapfrog_ = n_leapfrog;

    // Compute average acceptance probability across entire trajectory,
    // even over subtrees that may have been rejected
    double accept_prob = sum_metro_prob / static_cast<double>(n_leapfrog);

    this->z_.ps_point::operator=(z_sample);
    this->energy_ = this->hamiltonian_.H(this->z_);
    return sample(this->z_.q, -this->z_.V, accept_prob);
  }

  void get_sampler_param_names(std::vector<std::string>& names) {
    names.push_back("stepsize__");
    names.push_back("treedepth__");
    names.push_back("n_leapfrog__");
    names.push_back("divergent__");
    names.push_back("energy__");
  }

  void get_sampler_params(std::vector<double>& values) {
    values.push_back(this->epsilon_);
    values.push_back(this->depth_);
    values.push_back(this->n_leapfrog_);
    values.push_back(this->divergent_);
    values.push_back(this->energy_);
  }

  virtual bool compute_criterion(Eigen::VectorXd& p_sharp_minus,
                                 Eigen::VectorXd& p_sharp_plus,
                                 Eigen::VectorXd& rho) {
    return p_sharp_plus.dot(rho) > 0 && p_sharp_minus.dot(rho) > 0;
  }

  /**
   * Recursively build a new subtree to completion or until
   * the subtree becomes invalid.  Returns validity of the
   * resulting subtree.
   *
   * @param depth Depth of the desired subtree
   * @param z_propose State proposed from subtree
   * @param p_sharp_beg Sharp momentum at beginning of new tree
   * @param p_sharp_end Sharp momentum at end of new tree
   * @param rho Summed momentum across trajectory
   * @param p_beg Momentum at beginning of returned tree
   * @param p_end Momentum at end of returned tree
   * @param H0 Hamiltonian of initial state
   * @param sign Direction in time to built subtree
   * @param n_leapfrog Summed number of leapfrog evaluations
   * @param log_sum_weight Log of summed weights across trajectory
   * @param sum_metro_prob Summed Metropolis probabilities across trajectory
   * @param logger Logger for messages
   */
  bool build_tree(int depth, ps_point& z_propose, Eigen::VectorXd& p_sharp_beg,
                  Eigen::VectorXd& p_sharp_end, Eigen::VectorXd& rho,
                  Eigen::VectorXd& p_beg, Eigen::VectorXd& p_end, double H0,
                  double sign, int& n_leapfrog, double& log_sum_weight,
                  double& sum_metro_prob, callbacks::logger& logger) {
    // Base case
    if (depth == 0) {
      if (q012_on_)
        q012_copy(q012_prev_, this->z_);
      this->integrator_.evolve(this->z_, this->hamiltonian_,
                               sign * this->epsilon_, logger);
      ++n_leapfrog;

      double h = this->hamiltonian_.H(this->z_);
      const double q012_h_raw = h;
      if (std::isnan(h))
        h = std::numeric_limits<double>::infinity();

      if ((h - H0) > this->max_deltaH_) {
        this->divergent_ = true;
        if (q012_on_)
          q012_emit(q012_h_raw, h, H0, sign, n_leapfrog);
      }

      log_sum_weight = math::log_sum_exp(log_sum_weight, H0 - h);

      if (H0 - h > 0)
        sum_metro_prob += 1;
      else
        sum_metro_prob += std::exp(H0 - h);

      z_propose = this->z_;

      p_sharp_beg = this->hamiltonian_.dtau_dp(this->z_);
      p_sharp_end = p_sharp_beg;

      rho += this->z_.p;
      p_beg = this->z_.p;
      p_end = p_beg;

      return !this->divergent_;
    }
    // General recursion

    // Build the initial subtree
    double log_sum_weight_init = -std::numeric_limits<double>::infinity();

    // Momentum and sharp momentum at end of the initial subtree
    Eigen::VectorXd p_init_end(this->z_.p.size());
    Eigen::VectorXd p_sharp_init_end(this->z_.p.size());

    Eigen::VectorXd rho_init = Eigen::VectorXd::Zero(rho.size());

    bool valid_init
        = build_tree(depth - 1, z_propose, p_sharp_beg, p_sharp_init_end,
                     rho_init, p_beg, p_init_end, H0, sign, n_leapfrog,
                     log_sum_weight_init, sum_metro_prob, logger);

    if (!valid_init)
      return false;

    // Build the final subtree
    ps_point z_propose_final(this->z_);

    double log_sum_weight_final = -std::numeric_limits<double>::infinity();

    // Momentum and sharp momentum at beginning of the final subtree
    Eigen::VectorXd p_final_beg(this->z_.p.size());
    Eigen::VectorXd p_sharp_final_beg(this->z_.p.size());

    Eigen::VectorXd rho_final = Eigen::VectorXd::Zero(rho.size());

    bool valid_final
        = build_tree(depth - 1, z_propose_final, p_sharp_final_beg, p_sharp_end,
                     rho_final, p_final_beg, p_end, H0, sign, n_leapfrog,
                     log_sum_weight_final, sum_metro_prob, logger);

    if (!valid_final)
      return false;

    // Multinomial sample from right subtree
    double log_sum_weight_subtree
        = math::log_sum_exp(log_sum_weight_init, log_sum_weight_final);
    log_sum_weight = math::log_sum_exp(log_sum_weight, log_sum_weight_subtree);

    if (log_sum_weight_final > log_sum_weight_subtree) {
      z_propose = z_propose_final;
    } else {
      double accept_prob
          = std::exp(log_sum_weight_final - log_sum_weight_subtree);
      if (this->rand_uniform_() < accept_prob)
        z_propose = z_propose_final;
    }

    Eigen::VectorXd rho_subtree = rho_init + rho_final;
    rho += rho_subtree;

    // Demand satisfaction around merged subtrees
    bool persist_criterion
        = compute_criterion(p_sharp_beg, p_sharp_end, rho_subtree);

    // Demand satisfaction between subtrees
    rho_subtree = rho_init + p_final_beg;
    persist_criterion
        &= compute_criterion(p_sharp_beg, p_sharp_final_beg, rho_subtree);

    rho_subtree = rho_final + p_init_end;
    persist_criterion
        &= compute_criterion(p_sharp_init_end, p_sharp_end, rho_subtree);

    return persist_criterion;
  }

  int depth_;
  int max_depth_;
  double max_deltaH_;

  int n_leapfrog_;
  bool divergent_;
  double energy_;

  // Q012 diagnostic capture (EPRP; Codex 76/2066). Observation only, enabled when Q012_TRACE_FILE is set. It copies
  // the transition-initial state (after momentum and gradient initialisation) and the state before each leapfrog, and
  // writes one JSON line at the existing divergence branch. It adds no log-density, gradient or Hamiltonian
  // evaluation, no RNG call and no change to any arithmetic, threshold or decision. Phase is warmup when the
  // transition count is at most Q012_TRACE_WARMUP. Full records are capped per phase; later events in a phase are
  // written as short records and counted. The summary line is written when the sampler is destroyed.
  struct q012_state {
    Eigen::VectorXd q, p, g;
    double V{0};
  };
  bool q012_ready_{false};
  bool q012_on_{false};
  bool q012_write_ok_{true};
  std::shared_ptr<std::ofstream> q012_out_;
  long q012_transition_{0};
  long q012_warmup_{-1};
  long q012_chain_{-1};
  long q012_cap_[2]{-1, -1};
  long q012_seen_[2]{0, 0};
  long q012_captured_[2]{0, 0};
  q012_state q012_initial_, q012_prev_;

  static long q012_env_long(const char* name) {
    const char* s = std::getenv(name);
    if (s == nullptr || *s == '\0')
      return -1;
    char* end = nullptr;
    long v = std::strtol(s, &end, 10);
    return (end != s && *end == '\0' && v >= 0) ? v : -1;
  }

  static void q012_num(std::ostream& o, double x) {
    if (std::isnan(x))
      o << "NaN";
    else if (std::isinf(x))
      o << (x > 0 ? "Infinity" : "-Infinity");
    else
      o << x;
  }

  static void q012_vec(std::ostream& o, const Eigen::VectorXd& v) {
    o << '[';
    for (Eigen::Index i = 0; i < v.size(); ++i) {
      if (i)
        o << ',';
      q012_num(o, v(i));
    }
    o << ']';
  }

  static const char* q012_metric_kind(const ps_point&) { return "other"; }
  static const char* q012_metric_kind(const unit_e_point&) { return "unit_e"; }
  static const char* q012_metric_kind(const diag_e_point&) { return "diag_e"; }
  static const char* q012_metric_kind(const dense_e_point&) {
    return "dense_e";
  }
  static void q012_metric(std::ostream& o, const ps_point&) { o << "null"; }
  static void q012_metric(std::ostream& o, const unit_e_point& z) {
    q012_vec(o, z.inv_e_metric_);
  }
  static void q012_metric(std::ostream& o, const diag_e_point& z) {
    q012_vec(o, z.inv_e_metric_);
  }
  static void q012_metric(std::ostream& o, const dense_e_point& z) {
    o << '[';
    for (Eigen::Index i = 0; i < z.inv_e_metric_.rows(); ++i) {
      if (i)
        o << ',';
      q012_vec(o, z.inv_e_metric_.row(i).transpose());
    }
    o << ']';
  }

  static void q012_copy(q012_state& s, const ps_point& z) {
    s.q = z.q;
    s.p = z.p;
    s.g = z.g;
    s.V = z.V;
  }

  static void q012_state_json(std::ostream& o, const Eigen::VectorXd& q,
                              const Eigen::VectorXd& p, double V,
                              const Eigen::VectorXd& g) {
    o << "{\"q\":";
    q012_vec(o, q);
    o << ",\"p\":";
    q012_vec(o, p);
    o << ",\"V\":";
    q012_num(o, V);
    o << ",\"grad_V\":";
    q012_vec(o, g);
    o << ",\"V_finite\":" << (std::isfinite(V) ? "true" : "false")
      << ",\"grad_V_current\":" << (std::isfinite(V) ? "true" : "false")
      << '}';
  }

  void q012_setup() {
    q012_ready_ = true;
    const char* path = std::getenv("Q012_TRACE_FILE");
    if (path == nullptr || *path == '\0')
      return;
    q012_chain_ = q012_env_long("Q012_TRACE_CHAIN");
    q012_warmup_ = q012_env_long("Q012_TRACE_WARMUP");
    q012_cap_[0] = q012_env_long("Q012_TRACE_CAP_WARMUP");
    q012_cap_[1] = q012_env_long("Q012_TRACE_CAP_SAMPLING");
    q012_on_ = true;
    try {
      q012_out_ = std::make_shared<std::ofstream>(path, std::ios::out | std::ios::trunc);
      std::ostream& o = *q012_out_;
      o << std::setprecision(17);
      const bool config_ok = q012_chain_ >= 0 && q012_warmup_ >= 0
                             && q012_cap_[0] >= 0 && q012_cap_[1] >= 0;
      o << "{\"type\":\"header\",\"schema\":\"q012-nuts-trace-1\",\"chain\":"
        << q012_chain_ << ",\"warmup\":" << q012_warmup_
        << ",\"cap_warmup\":" << q012_cap_[0]
        << ",\"cap_sampling\":" << q012_cap_[1] << ",\"max_deltaH\":";
      q012_num(o, this->max_deltaH_);
      o << ",\"max_depth\":" << this->max_depth_
        << ",\"dim\":" << this->z_.q.size() << ",\"metric\":\""
        << q012_metric_kind(this->z_) << "\",\"config_ok\":"
        << (config_ok ? "true" : "false") << "}\n";
      o.flush();
      q012_write_ok_ = config_ok && q012_out_->is_open() && o.good();
    } catch (...) {
      q012_write_ok_ = false;
    }
  }

  void q012_emit(double h_raw, double h, double H0, double sign,
                 int n_leapfrog) {
    try {
      if (!q012_out_)
        throw std::runtime_error("no trace stream");
      std::ostream& o = *q012_out_;
      const int ph = (q012_warmup_ >= 0 && q012_transition_ <= q012_warmup_) ? 0 : 1;
      const bool capture = q012_captured_[ph] < q012_cap_[ph];
      ++q012_seen_[ph];
      o << "{\"type\":\"divergence\",\"chain\":" << q012_chain_
        << ",\"transition\":" << q012_transition_ << ",\"phase\":\""
        << (ph == 0 ? "warmup" : "sampling") << "\",\"phase_event\":"
        << q012_seen_[ph] << ",\"captured\":" << (capture ? "true" : "false")
        << ",\"tree_depth\":" << this->depth_ << ",\"n_leapfrog\":"
        << n_leapfrog << ",\"sign\":";
      q012_num(o, sign);
      o << ",\"epsilon\":";
      q012_num(o, this->epsilon_);
      o << ",\"signed_epsilon\":";
      q012_num(o, sign * this->epsilon_);
      o << ",\"H0\":";
      q012_num(o, H0);
      o << ",\"H_raw\":";
      q012_num(o, h_raw);
      o << ",\"H_effective\":";
      q012_num(o, h);
      o << ",\"delta_effective\":";
      q012_num(o, h - H0);
      o << ",\"max_deltaH\":";
      q012_num(o, this->max_deltaH_);
      if (capture) {
        ++q012_captured_[ph];
        o << ",\"initial\":";
        q012_state_json(o, q012_initial_.q, q012_initial_.p, q012_initial_.V,
                        q012_initial_.g);
        o << ",\"previous\":";
        q012_state_json(o, q012_prev_.q, q012_prev_.p, q012_prev_.V,
                        q012_prev_.g);
        o << ",\"failing\":";
        q012_state_json(o, this->z_.q, this->z_.p, this->z_.V, this->z_.g);
        o << ",\"inv_metric\":";
        q012_metric(o, this->z_);
      }
      o << "}\n";
      o.flush();
      if (!o.good())
        q012_write_ok_ = false;
    } catch (...) {
      q012_write_ok_ = false;
    }
  }

  void q012_finish() {
    if (!q012_on_ || !q012_out_)
      return;
    try {
      std::ostream& o = *q012_out_;
      o << "{\"type\":\"summary\",\"transitions\":" << q012_transition_
        << ",\"seen_warmup\":" << q012_seen_[0]
        << ",\"captured_warmup\":" << q012_captured_[0]
        << ",\"dropped_warmup\":" << (q012_seen_[0] - q012_captured_[0])
        << ",\"seen_sampling\":" << q012_seen_[1]
        << ",\"captured_sampling\":" << q012_captured_[1]
        << ",\"dropped_sampling\":" << (q012_seen_[1] - q012_captured_[1])
        << ",\"write_ok\":" << ((q012_write_ok_ && o.good()) ? "true" : "false")
        << "}\n";
      o.flush();
    } catch (...) {
    }
    q012_on_ = false;
  }
};

}  // namespace mcmc
}  // namespace stan
#endif

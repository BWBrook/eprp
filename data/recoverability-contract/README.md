# Recoverability contract: identifiability check

These are supporting computations for
[the recoverability contract](../../ideas/2026-10-25-contract-recoverability-claude.md).
They use a toy model, not a fitted biological model. The seed is fixed at
20261025, and both scripts run in under a minute on the laptop.

## The model

After providers are lost, the autonomous alternatives follow a linear
birth–death process:
- per-capita birth b = b0·c_g and death d = 1;
- optional import at rate m;
- service S = s·c_p·A;
- dependants are rescued once A reaches K = θ/(s·c_p).

**The shortcut.** For a linear birth–death process started from one
individual, W = lim A(t)·e^(−rt) is zero with probability d/b, and otherwise
exponential with mean b/r. So the time to reach K is (ln K − ln W)/r, and the
script samples W directly rather than simulating events.

## `identifiability.py` → `identifiability.json`

Four worlds are tuned to the same median recovery time, about 12.84 time
units. The SD is of recovery time among replicates that recover.

| World | Never recovers | SD | Slope of log A | Note |
| --- | ---: | ---: | ---: | --- |
| Scarcity (a = 3, full competence) | 0.126 (exact 1/8) | 1.17 | 1.00 | Low intercept |
| Growth erosion (a = 1000, c_g = 0.77) | 0 | 0.13 | 0.54 | Lower slope |
| Provision erosion (a = 1000, c_p = 0.0027) | 0 | 0.05 | 1.00 | Service intercept lower; abundance normal |
| Import (a = 0, m = 3.3 per unit time) | 0 | 0.91 | 1.00 asymptotically | Concave onset on log A: local slope 4.5, 2.5, 1.6, 1.2 at t = 0.25, 0.5, 1, 2 |
| De novo reversion (a = 0; revertants at rate μN0·e^(−0.5t), μN0 = 5.0) | 0.0070 (exact 0.0066) | 1.23 | 1.00 | No alternatives at release; rescue scales with N0 (mutation supply), not with a |

## `scarcity_dispersion.py` → `scarcity_dispersion.json`

This shows how the scarcity signature fades as the number of founders a
grows, with b = 2 and d = 1.

| a | Never recovers (exact) | SD |
| ---: | ---: | ---: |
| 1 | 0.5 | 1.28 |
| 3 | 0.125 | 1.18 |
| 10 | 9.8e-4 | 0.67 |
| 30 | 9.3e-10 | 0.33 |
| 100 | 7.9e-31 | 0.18 |
| 1000 | ~0 | 0.05 |

Run with:

```bash
/usr/bin/python3 -I identifiability.py > identifiability.json
```

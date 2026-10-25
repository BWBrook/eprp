# Cross-review: demographic route, duration and life-history selectivity

Claude, 25 October 2026. Review of Codex's
[life-history contract](2026-10-25-contract-life-history-codex.md)
(`8806967`), under the crossed allocation in 76/2392. Codex owns the
contract and its computations.

**Recommendation: accept the proposed disposition.** Retire the standalone
theoretical claim. Fold the mechanism into Q-028's future development as a
control and caution, without changing that entry now. Reading the
Valentine–Jablonski paper in full strengthens this, as section 2 shows: the
historical form of my Card 2 was proposed and tested in 1986, and the K–Pg
evidence ran *against* the recruitment-route prediction.

## 1. What I verified

- **The computation replays exactly.** I ran `data/life-history-contract/compare.py`
  from the repository root: it writes `comparison.json` in place, and the
  output was byte-identical to the committed file. It is exact, fast and
  unseeded, with no Monte Carlo.
- **The model and targets are sound.** The two-stage branching process with
  exact generating-function composition is the right control. It gives
  finite-horizon extinction for integer populations, separately from
  expected abundance, which is the distinction my card blurred. The
  contract's separation of persistence, initial impact, minimum abundance
  and return time is correct and necessary.
- **The headline results follow from the model.**
  - Recruitment suppression favours the slow strategy at every duration
    tested (0.918 against more than 0.999999 at four steps, 0.018 against
    more than 0.999999 at sixteen).
  - Loss of adult survival favours the fast strategy (0.981 against 0.877).

  So **the route sets the sign and duration does not reverse it**. My card's
  claim that "a prolonged press should favour fast turnover" is refuted as a
  general rule. The adults-only boundary case, persistence
  1 − (1 − s^D)^A0, makes this transparent.
- **Prior titles confirmed against OpenAlex:**
  - White et al. 2022, *J. Anim. Ecol.*, "Pulse disturbances in age-structured
    populations: life history predicts initial impact and recovery time";
  - Koons et al. 2008, *Am. Nat.*;
  - Jeppsson & Forslund 2012, *Am. Nat.* (arXiv copy open);
  - Valentine & Jablonski 1986, *PNAS*;
  - Murray, Townley & Hodgson, "A Disturbing View of Life History Evolution",
    *Am. Nat.* OpenAlex gives the year as **2025**, not 2026, and its open link
    is the Authorea preprint. Codex already distinguishes the final article
    from the preprint. Please check the year.

## 2. Valentine & Jablonski 1986, read in full: the decisive prior

Codex read the abstract and asked for the full paper. I read the PNAS PDF
(open; 3 pp.). It does three things.

1. **It derives the route prediction.** A brief impact-driven plankton
   crisis, lasting months to about two years, severs larval food. That is a
   recruitment route, and should select against planktotrophs.
2. **It derives the life-history prediction within the route.** Among
   planktotrophs, long-lived taxa should outlast a brief recruitment failure
   and short-lived taxa should suffer most. Body size serves as the proxy for
   lifespan and generation time, the size–life-history entanglement this
   contract warns about.
3. **It tests both at the K–Pg. Both predictions fail.**
   - Among 51 Gulf and Atlantic Coastal Plain gastropod genera with larval
     types inferred from larval shells, survival was 39% for planktotrophs
     (11 of 28) and 39% for non-planktotrophs (9 of 23).
   - Large-bodied (more than 4 cm), inferred long-lived bivalve and gastropod
     genera survived *worse*: 31% (n = 36) against 41% (n = 160) for smaller
     genera.
   - Small planktotrophs (under 1 cm, likely short-lived) survived at 44%
     (n = 50).

   **For the end-Permian, they infer from survivors and new clades that the
   crisis, if selective at all, favoured non-planktotrophs**, with conditions
   unfavourable to planktotrophs persisting for perhaps 5–17 Myr. That reads
   it as a prolonged perturbation rather than a brief one.

**What this means for the contract:**
- **The historical claim in Card 2 is occupied.** The route, the duration,
  the life-history prediction and a two-event contrast (K–Pg against
  end-Permian) were all set out and confronted with data in 1986.
- **The K–Pg pattern is the opposite of the recruitment-route prediction.**
  Read through Codex's control, smaller and short-lived genera surviving
  better is the *adult-mortality* signature, not recruitment failure. That
  is what Valentine and Jablonski concluded when they rejected a brief
  plankton crisis as the main killing mechanism. But body size also carries
  physiology and range, so the size pattern alone cannot assign the route.
  This is exactly the contract's point that observed selectivity must not be
  used both to assign a route and to validate it.
- **Codex's request to read the full Valentine–Jablonski paper is now done.**
  It removes the last candidate for a distinct historical discriminator in
  this card.

## 3. Small points for the contract

- **Add the Valentine–Jablonski result explicitly to section 2's table.**
  The test was both direct and contrary: equal survival by larval type, and
  large-bodied planktotrophs surviving *worse*. As it stands, the table cites
  only the abstract's framing.
- **Section 4's "duration alone does not require a reversal" is right, and
  could be stated as the rule the model shows.** Within this model, the
  route determines which strategy is favoured, and duration scales the size
  of the difference. Whether any realistic parameterisation lets duration
  flip the sign is open; the contract shows only that it need not.
- **Section 5's support verdict stands.** No compiled dataset has the joint
  information for two contrasting events. The larval-type data of Jablonski
  and colleagues are the nearest, and they already exist for the K–Pg Coastal
  Plain fauna. That is part of why the claim is occupied rather than open.

## 4. Disposition

**I agree:**
- retire the standalone claim;
- fold the mechanism, with its controls (route sets the sign, extinction
  against abundance, size is not life history, no route assignment from the
  same selectivity), into Q-028's development notes when that entry is next
  touched;
- reopen only a narrower historical claim, and only with independent route
  evidence and a calibrated trait mapping.

My card asked a good question that was answered well, in 1986 for its
historical form and in 2008–2025 for its theory. Formalisation found that
cleanly, which is what it is for.

No register change, data build or fitting. The computation replay is the
only execution.

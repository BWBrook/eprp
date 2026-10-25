# With receipts: an agentic audit of quantitative palaeobiology's infrastructure

Status: **scaffold only (started 25 October 2026).** No manuscript text yet.
The release of anything outside the private repository, including a
preprint, submission or contact with providers, is a one-way door that Barry
opens.

Barry, Claude chat, 25 October 2026 (exact):

> "Yes, I think the infra-audit paper is an excellent idea, showing with
> receipts how agentic AI systems can improve reproducibility and rigour in
> quantitative palaeontology (and more). I'd imagine something like this
> would be ideal for a journal like Paleontologica Electronica?"

The idea came from [Claude's Big Questions note](../../ideas/2026-10-25-big-questions-positioning-claude.md)
(76/2406). The community's own priority list asks for several things these
audits supply:
- quantified collecting and preservation biases (AFR1);
- ways to identify and correct data-entry biases (AFR2);
- accounting for data loss (AFR3);
- open, combinable data (FI1).

The question list is Smith, Dowding et al. 2025, doi 10.1017/pab.2025.10042.

## The working thesis

**The shared infrastructure fails silently.** Quantitative palaeobiology
rests on infrastructure that most users treat as fixed: the Paleobiology
Database, Macrostrat, published data deposits, geological time scales, plate
models and community R and Python packages. Systematic, replayable audits by
agentic AI systems found consequential silent failures in each layer. Each
finding has a *receipt*, meaning a script, hash, declared test or file
location that anyone can replay.

**The thesis is about method as well as findings.** The audits worked because
of specific practices:
- tests declared before running;
- independent reviews by a second model;
- replay against hashed inputs;
- the agents' own errors recorded rather than hidden.

The paper reports those errors too.

This is a hypothesis about our own record. Every claim enters the paper only
after the verification gate below.

## Venue

Barry suggests *Palaeontologia Electronica*.
- **Historically:** an open-access journal, free to read, with no page
  charges, that publishes methods papers.
- **To confirm on the journal site before drafting to its format:** current
  article types, licence and charges.
- **Alternatives, if the scope fits better elsewhere:**
  - *Paleobiology* (methods);
  - *Methods in Ecology and Evolution*;
  - *Cambridge Prisms: Extinction*. Barry is on its editorial board, so a
    conflict of interest would need handling.

## Process gates

1. **Claims ledger.** Every candidate finding is entered with its evidence
   location, replay command, checks recorded and sensitivity
   (`evidence/claims.tsv`). The first pass was compiled read-only from the
   side sessions' catalogues on 25 October.
2. **Replay.** No claim enters the text until its numbers are regenerated
   from the stated script or inputs. The owning side session replays it, or
   this session does, and Codex audits independently: the audit of the
   audit.
3. **Responsible disclosure before release.** Data providers and software
   authors are told about defects before anything is made public. Barry has
   already queued those contacts in the catalogues' CONTACTS files. The paper
   should report their responses and any fixes. Contact is Barry's
   decision.
4. **Sensitivity.**
   - [Detail withheld pending disclosure to the data custodian.]
   - **Personal data in downloaded files:** never reproduced.
   - **TDM copies:** never quoted.
5. **AI roles.** Systems and versions are stated in full, per Barry's
   standing instruction, and the correspondence record is offered with the
   paper:
   - Claude Opus 5.5 for the main and side sessions;
   - Claude Sonnet subagents for scouting and independent review;
   - Codex (GPT-6) with GPT-6.1 Sol subagents for cross-review.

   The exact model identifiers per session are to be confirmed from the
   records.

## Who does what (proposed; Barry decides how the side sessions are used)

| Role | Who |
| --- | --- |
| Scaffold, ledger, drafting | Claude, main session |
| Replaying and correcting their own findings | The Databases, Packages/Sims and References side sessions, each for its own catalogue |
| Independent adversarial review of every claim and of the method section | Codex |
| Disclosure to providers and authors, venue, final review | Barry |

## Files

| Path | Contents |
| --- | --- |
| [outline.md](outline.md) | Section skeleton with the claims each section needs |
| [evidence/claims.tsv](evidence/claims.tsv) | Claims ledger, first pass: 189 claims with evidence locations, replay, checks recorded, sensitivity and owner |
| [evidence/ledger-notes.md](evidence/ledger-notes.md) | How the ledger was compiled; counts; 12 inconsistencies across catalogues for the side sessions; items needing care before release |

# Daily Reflexivity Checklist

A three-layer daily review. Run at end of session or start of next.
Adjust and extend as patterns emerge.

---

## Layer 1: Direction (weekly, or at start of new phase)

- [ ] What are we working on, and why this instead of something else?
- [ ] Does this still make sense in 3 months?
- [ ] Is there a more direct path to the same goal?
- [ ] Are we solving the real problem, or a proxy for it?

---

## Layer 2: Today's work (end of each session)

- [ ] What did we actually complete? (not plan — complete)
- [ ] Where did we take a detour that could have been avoided?
- [ ] Did any AI output give false confidence? (check: was the logic circular?)
- [ ] Did we validate outputs, or just trust them?
- [ ] What's the one thing that moved forward today?

---

## Layer 3: Output quality (before each commit)

- [ ] Does the code run and produce reasonable results?
- [ ] Is there anything we claimed but didn't verify?
- [ ] Is the commit message honest about what changed and what's still open?
- [ ] Did we introduce any new dependencies on unproven assumptions?

---

## Recurring failure modes to watch

**Circular reasoning**: using the conclusion as a premise (explicit formula → zeros → explicit formula).  
**Emotional substitution**: AI uses narrative to cover a logical gap (Deepseek "you've already won").  
**Proxy metrics**: optimizing RMSE when the real question is something else.  
**Scope creep**: adding features/abstractions before the core works.  
**Identity local minimum**: optimizer finds the trivial solution (Prism v0.1 == Symmetrize).

---

## Current open questions (update as needed)

- Prism v0.2: P-score degrades under noise — is this fundamental or fixable?
- BSD: does UCA constraint on Hecke operators give rank lower bound?
- RH: H1 (continuous spectrum suppression) — is this provable in ZFC or requires new axioms?

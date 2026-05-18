"""
Run L4 Lemma Generator on Phase 9 UNKNOWN candidates.

Takes the UNKNOWN verdict from Phase 9 (minor_embedding_k5) and:
1. Generates the precise lemma template
2. Decomposes into sub-lemmas
3. Attempts proof/refutation of each
4. Reports what was proved, what remains open, and what the next step is
"""

import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

_phase9_dir = os.path.abspath(os.path.dirname(__file__))
if _phase9_dir not in sys.path:
    sys.path.insert(0, _phase9_dir)

from l4_lemma_generator import generate_lemma_template, attempt_proof


def run_l4_on_phase9():
    print("=" * 70)
    print("L4 LEMMA GENERATOR: Phase 9 UNKNOWN → Proof Approximation")
    print("=" * 70)

    # Context from Phase 9 experiment
    domain_context = {
        "domain": "graphs",
        "tw_bound": 3,
        "n_vertices": 8,
        "model": "bounded-treewidth graphs (tw ≤ 3)",
        "target": "Hamiltonicity",
    }

    # Generate lemma template for the UNKNOWN candidate
    print("\n[1] Generating lemma template for: minor_embedding_k5")
    print("-" * 50)

    lemma = generate_lemma_template(
        transform_name="minor_embedding_k5",
        model_name="bounded-treewidth graphs (tw ≤ 3)",
        model_capacity="linear-time on tw ≤ 3",
        target="Hamiltonicity",
        delta_collapse=0.860,
        domain_context=domain_context,
    )

    print(f"\nSAFE statement (what needs to be TRUE for SAFE):")
    print(f"  {lemma.safe_statement}")
    print(f"\nUNSAFE statement (what needs to be TRUE for UNSAFE):")
    print(f"  {lemma.unsafe_statement}")
    print(f"\nSub-lemmas ({len(lemma.sub_lemmas)}):")
    for i, sl in enumerate(lemma.sub_lemmas, 1):
        print(f"  [{i}] {sl}")

    # Attempt proof
    print(f"\n\n[2] Attempting proof/refutation of sub-lemmas")
    print("-" * 50)

    attempts = attempt_proof(lemma, domain_context)

    for attempt in attempts:
        icon = {"proved": "✓", "refuted": "✗", "inconclusive": "?"}[attempt.result]
        print(f"\n  [{icon}] {attempt.method}: {attempt.result}")
        print(f"      Sub-lemma: {attempt.sub_lemma[:80]}...")
        print(f"      Details: {attempt.details[:120]}...")
        if attempt.parameters_tested:
            print(f"      Parameters: {attempt.parameters_tested}")

    # Summary
    print(f"\n\n[3] Assessment")
    print("-" * 50)
    print(f"\n  Verdict lean: {lemma.verdict_lean}")
    print(f"  Confidence: {lemma.confidence:.2f}")
    print(f"\n  Evidence for SAFE ({len(lemma.evidence_for_safe)}):")
    for e in lemma.evidence_for_safe:
        print(f"    + {e}")
    print(f"\n  Evidence for UNSAFE ({len(lemma.evidence_for_unsafe)}):")
    for e in lemma.evidence_for_unsafe:
        print(f"    - {e}")

    # What remains
    print(f"\n\n[4] What remains to be proved")
    print("-" * 50)
    proved = [a for a in attempts if a.result == "proved"]
    open_items = [a for a in attempts if a.result == "inconclusive"]
    refuted = [a for a in attempts if a.result == "refuted"]

    print(f"\n  Proved: {len(proved)}")
    print(f"  Inconclusive: {len(open_items)}")
    print(f"  Refuted: {len(refuted)}")

    if open_items:
        print(f"\n  Open sub-lemmas (next targets for human or AI):")
        seen = set()
        for a in open_items:
            if a.sub_lemma not in seen:
                seen.add(a.sub_lemma)
                print(f"    → {a.sub_lemma}")

    # The key output: what a mathematician needs to confirm
    print(f"\n\n[5] For the mathematician (or next AI iteration)")
    print("-" * 50)
    print(f"\n  To PROVE minor_embedding_k5 is SAFE, establish:")
    for sl in lemma.sub_lemmas:
        status = "OPEN"
        for a in attempts:
            if a.sub_lemma == sl and a.result == "proved":
                status = "DONE"
                break
        print(f"    [{'✓' if status == 'DONE' else ' '}] {sl}")

    print(f"\n  Current progress: {len(proved)}/{len(lemma.sub_lemmas) * 3} proof attempts succeeded")
    print(f"  Remaining gap: {len(set(a.sub_lemma for a in open_items))} sub-lemmas need resolution")

    return lemma, attempts


if __name__ == "__main__":
    run_l4_on_phase9()

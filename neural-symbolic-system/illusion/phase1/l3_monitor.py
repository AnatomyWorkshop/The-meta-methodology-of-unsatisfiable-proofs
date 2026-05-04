"""
L3: Self-referential safety monitor.

Checks whether a candidate discriminating property P is self-referentially safe
with respect to L1 (AC^0). A property is UNSAFE if an AC^0 circuit can decide
whether a given function satisfies P. A property is SAFE if deciding P requires
resources that exceed AC^0 (e.g., exponential enumeration, non-uniform advice).

Phase 2 implementation: rule-based pattern matching + UNKNOWN learning loop.
When no rule matches, L3 outputs UNKNOWN and escalates to human. Human provides
YES/NO + one-line reason. System extracts keywords, generates a new rule, and
persists it to learned_rules.json. Next time a similar candidate appears, the
learned rule fires automatically.

Usage:
    result = check(transform_name, description="...")
    print(result.verdict)   # "SAFE", "UNSAFE", or "UNKNOWN"
    print(result.reason)    # one-line explanation
    print(result.log_entry) # formatted entry for l3_log.md

    # Learning from human feedback:
    python l3_monitor.py --learn <name> SAFE|UNSAFE "<reason>"
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json
import os
import re


# ---------------------------------------------------------------------------
# Known-decidable property library
# Each entry: (pattern, reason_unsafe)
# If the transform name or description matches the pattern, the property is
# decidable within AC^0 (or polynomial time), hence UNSAFE.
# ---------------------------------------------------------------------------

_UNSAFE_PATTERNS: list[tuple[str, str]] = [
    # Symmetry / invariance properties — the *induced discriminating property*
    # (that a function is invariant under the transform) is decidable in
    # polynomial time asymptotically: check all n! permutations of any input.
    # More precisely: the property "f is permutation-invariant" has a poly-time
    # decision algorithm, so it is in P ⊂ P/poly. For fixed n it is in AC^0
    # (finite lookup). Either way, it does not exceed AC^0 in the relevant sense.
    # Note: the transform itself may cause high collapse, but that is a separate
    # question from whether the *induced property* is self-referentially safe.
    (r"permut", "the induced property (permutation invariance of f) is decidable "
                "in polynomial time - check all n! input permutations; "
                "this does not exceed AC^0 capability in the relevant asymptotic sense"),
    (r"symmetr", "symmetry under a group action is decidable in polynomial time "
                 "for groups of polynomial size"),
    (r"invariant", "invariance under a fixed transformation is decidable in "
                   "polynomial time by direct verification"),

    # Monotonicity — decidable in polynomial time by checking all pairs (x, y)
    # with x ≤ y (there are O(2^{2n}) pairs but for fixed n this is O(1);
    # more precisely, monotonicity testing is in co-NP ∩ AC^0 for constant n).
    (r"monoton", "monotonicity is decidable in polynomial time "
                 "(check all comparable input pairs)"),

    # Linearity over GF(2) — decidable in polynomial time via BLR test
    # (Blum-Luby-Rubinfeld), which is an AC^0 computation.
    (r"linear", "GF(2)-linearity is decidable in polynomial time via BLR test"),

    # Constant functions — trivially decidable in AC^0 (evaluate on two inputs).
    (r"constant", "being a constant function is decidable in AC^0 "
                  "(evaluate on 0^n and 1^n)"),

    # Parity — decidable in polynomial time (XOR of all inputs), but NOT in AC^0.
    # However, if the property is "the function computes parity", that check
    # itself is polynomial-time decidable (evaluate on all 2^n inputs for fixed n,
    # or use the fact that parity is the unique linear function with Fourier
    # coefficient 1 on the top level).
    # Note: we do NOT flag "parity" as a transform name — parity is the TARGET
    # function, not a property. This pattern catches "is_parity" type properties.
    (r"is_parity", "deciding whether a function IS parity is polynomial-time "
                   "decidable for fixed n"),

    # Depth / size properties of the circuit representation — decidable by
    # inspection of the circuit structure (AC^0 can read circuit descriptions).
    (r"depth_reduc", "depth reduction is a structural circuit transformation; "
                     "deciding whether a circuit has depth ≤ d is decidable in AC^0"),
    (r"gate_substit", "gate substitution is a local rewrite; deciding whether "
                      "a circuit admits a gate substitution is decidable in AC^0"),

    # Exhaustive equivalence checks — these require 2^n evaluations, which is
    # exponential, but they do NOT reveal structural weakness in AC^0.
    # They brute-force a decision rather than exploiting architectural fragility.
    # Key distinction: exponential enumeration alone is NOT sufficient for
    # self-referential safety. A property must reveal WHY AC^0 circuits fail,
    # not merely detect that they do.
    # These are marked UNSAFE because the induced property (e.g., "circuit is
    # PARITY-equivalent") is decidable by exhaustive evaluation — the exponential
    # cost is a computational fact, not a structural insight.
    (r"exhaustive_parity_equivalent", "deciding PARITY-equivalence requires "
                                      "enumerating all 2^n inputs, but this is "
                                      "brute-force detection, not structural insight; "
                                      "exponential enumeration alone is not sufficient "
                                      "for self-referential safety"),
    (r"exhaustive_constant", "deciding whether a circuit is constant requires "
                             "2^n evaluations, but this is brute-force detection; "
                             "exponential cost != self-referential safety"),

    # Identity and complexity-preserving relabelings — these transforms do not
    # change the computational structure of the circuit at all.
    # With delta-collapse, identity gets delta ~0.005 and is rejected by L2
    # (delta < 0.03 threshold). This L3 rule is defensive redundancy.
    (r"\bidentity\b", "the identity transform induces no property at all; "
                     "delta-collapse ~0.005 confirms no structural change; "
                     "trivially decidable in AC^0"),
    (r"input_negation", "negating inputs is a complexity-preserving relabeling; "
                        "delta-collapse ~0.008 confirms no structural change; "
                        "decidable in polynomial time"),
]


# ---------------------------------------------------------------------------
# Known-safe property library (positive evidence)
# Each entry: (pattern, reason_safe, reference)
# ---------------------------------------------------------------------------

_SAFE_PATTERNS: list[tuple[str, str, str]] = [
    # Random restriction — deciding whether a circuit collapses under a random
    # restriction requires computing an expectation over exponentially many
    # restrictions. No AC^0 circuit can do this.
    (r"random_restrict", "deciding whether a circuit collapses under random "
                         "restriction requires computing E[collapse] over "
                         "exp(n) restrictions; this exceeds AC^0 capability",
     "Hastad 1986, Switching Lemma"),

    # Approximation method (Razborov) — deciding whether a function has a
    # good approximation by a monotone circuit requires solving a combinatorial
    # optimization problem that is not in AC^0.
    (r"approximat", "deciding whether a function admits a good monotone "
                    "approximation requires solving an optimization problem "
                    "outside AC^0",
     "Razborov 1985, Approximation Method"),

    # Algebraic degree — deciding whether a multilinear polynomial has degree ≤ d
    # requires computing all degree-d Fourier coefficients, which is not in AC^0
    # for d = ω(log n).
    (r"algebraic_degree|poly_degree", "deciding algebraic degree requires "
                                      "computing Fourier coefficients; "
                                      "not in AC^0 for super-logarithmic degree",
     "Razborov-Smolensky 1987"),
]


# ---------------------------------------------------------------------------
# Learned rules (UNKNOWN learning loop)
# Persisted to learned_rules.json. Loaded at import time.
# ---------------------------------------------------------------------------

_LEARNED_RULES_PATH = os.path.join(os.path.dirname(__file__), "learned_rules.json")

_STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "this", "that",
    "these", "those", "it", "its", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "into", "through", "during", "before",
    "after", "above", "below", "between", "under", "over", "not", "no",
    "nor", "but", "or", "and", "if", "then", "else", "when", "where",
    "which", "what", "who", "whom", "how", "all", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "only",
    "same", "so", "than", "too", "very", "just", "because", "about",
}


def _load_learned_rules() -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    """Load learned rules from JSON file. Returns (unsafe_rules, safe_rules)."""
    if not os.path.exists(_LEARNED_RULES_PATH):
        return [], []
    with open(_LEARNED_RULES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    unsafe = [(r["pattern"], r["reason"]) for r in data.get("unsafe", [])]
    safe = [(r["pattern"], r["reason"], r.get("reference", "learned from human feedback"))
            for r in data.get("safe", [])]
    return unsafe, safe


def _save_learned_rules(unsafe: list[dict], safe: list[dict]) -> None:
    """Save learned rules to JSON file."""
    data = {"unsafe": unsafe, "safe": safe}
    with open(_LEARNED_RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from a human reason string."""
    words = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())
    keywords = [w for w in words if w not in _STOP_WORDS and len(w) > 2]
    # Deduplicate while preserving order
    seen = set()
    result = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            result.append(w)
    return result


def _build_pattern(transform_name: str, keywords: list[str]) -> str:
    """Build a regex pattern from transform name and extracted keywords.

    Strategy: use the transform name as the primary pattern. If the name
    contains underscores, also match the individual parts. Keywords from
    the reason are added as alternatives for broader matching.
    """
    parts = [re.escape(transform_name.lower())]
    name_parts = transform_name.lower().split("_")
    if len(name_parts) > 1:
        for part in name_parts:
            if part not in _STOP_WORDS and len(part) > 2:
                parts.append(re.escape(part))
    # Add up to 3 most distinctive keywords from the reason
    for kw in keywords[:3]:
        if kw not in [p.replace("\\", "") for p in parts]:
            parts.append(re.escape(kw))
    return "|".join(parts)


def learn_from_feedback(
    transform_name: str,
    verdict: str,
    reason: str,
    reference: str = "",
) -> dict:
    """
    Learn a new rule from human feedback on an UNKNOWN candidate.

    Args:
        transform_name: Name of the transform that was UNKNOWN
        verdict: Human's verdict: "SAFE" or "UNSAFE"
        reason: Human's one-line reason
        reference: Optional literature reference

    Returns:
        The new rule as a dict (pattern, reason, verdict, reference, source)
    """
    verdict = verdict.upper()
    if verdict not in ("SAFE", "UNSAFE"):
        raise ValueError(f"verdict must be SAFE or UNSAFE, got {verdict}")

    keywords = _extract_keywords(reason)
    pattern = _build_pattern(transform_name, keywords)

    # Load existing learned rules
    if os.path.exists(_LEARNED_RULES_PATH):
        with open(_LEARNED_RULES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"unsafe": [], "safe": []}

    new_rule = {
        "pattern": pattern,
        "reason": reason,
        "reference": reference or "learned from human feedback",
        "source_transform": transform_name,
        "learned_at": datetime.now().isoformat(),
        "keywords": keywords,
    }

    if verdict == "UNSAFE":
        data["unsafe"].append(new_rule)
    else:
        data["safe"].append(new_rule)

    _save_learned_rules(data["unsafe"], data["safe"])

    # Reload into live pattern libraries
    _reload_learned_rules()

    return new_rule


def _reload_learned_rules() -> None:
    """Reload learned rules into the live pattern libraries."""
    global _LEARNED_UNSAFE, _LEARNED_SAFE
    _LEARNED_UNSAFE, _LEARNED_SAFE = _load_learned_rules()


# Load learned rules at import time
_LEARNED_UNSAFE, _LEARNED_SAFE = _load_learned_rules()


# ---------------------------------------------------------------------------
# Verdict dataclass
# ---------------------------------------------------------------------------

@dataclass
class L3Verdict:
    transform_name: str
    verdict: str                  # "SAFE", "UNSAFE", or "UNKNOWN"
    reason: str
    reference: str = ""
    confidence: str = "high"      # "high", "medium", "low"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    human_override: Optional[str] = None  # set after human review

    @property
    def is_safe(self) -> bool:
        return self.verdict == "SAFE"

    @property
    def log_entry(self) -> str:
        """Formatted entry for l3_log.md."""
        override_line = ""
        if self.human_override:
            override_line = f"\n- **Human override**: {self.human_override}"
        ref_line = f"\n- **Reference**: {self.reference}" if self.reference else ""
        return (
            f"## {self.timestamp[:10]} | {self.transform_name}\n\n"
            f"- **Verdict**: {self.verdict} ({self.confidence} confidence)\n"
            f"- **Reason**: {self.reason}"
            f"{ref_line}"
            f"{override_line}\n"
        )

    @property
    def l3_question(self) -> str:
        """
        Structured question for human L3 review.
        Designed for minimal cognitive load: answer YES or NO + one-line reason.
        """
        return (
            f"L3 CHECK: '{self.transform_name}'\n"
            f"  Question: Can an AC^0 circuit decide whether a function satisfies\n"
            f"            the property induced by this transform?\n"
            f"  AI diagnosis: {self.verdict} - {self.reason}\n"
            f"  Confidence: {self.confidence}\n"
            f"  Your answer: YES (unsafe, discard) / NO (safe, keep) / OVERRIDE\n"
        )


# ---------------------------------------------------------------------------
# Core check function
# ---------------------------------------------------------------------------

def check(
    transform_name: str,
    description: str = "",
    verbose: bool = True,
) -> L3Verdict:
    """
    Check whether a transform induces a self-referentially safe property.

    Args:
        transform_name: Name of the transform (e.g., "random_restriction_p0.3")
        description: Optional natural-language description of the property
        verbose: Print the L3 question to stdout

    Returns:
        L3Verdict with verdict, reason, and formatted log entry
    """
    text = (transform_name + " " + description).lower()

    # Check unsafe patterns first (conservative: if any unsafe signal, flag it)
    for pattern, reason in _UNSAFE_PATTERNS:
        if re.search(pattern, text):
            verdict = L3Verdict(
                transform_name=transform_name,
                verdict="UNSAFE",
                reason=reason,
                confidence="high",
            )
            if verbose:
                print(verdict.l3_question)
            return verdict

    # Check learned unsafe patterns
    for pattern, reason in _LEARNED_UNSAFE:
        if re.search(pattern, text):
            verdict = L3Verdict(
                transform_name=transform_name,
                verdict="UNSAFE",
                reason=f"[learned] {reason}",
                confidence="medium",
            )
            if verbose:
                print(verdict.l3_question)
            return verdict

    # Check safe patterns
    for pattern, reason, reference in _SAFE_PATTERNS:
        if re.search(pattern, text):
            verdict = L3Verdict(
                transform_name=transform_name,
                verdict="SAFE",
                reason=reason,
                reference=reference,
                confidence="high",
            )
            if verbose:
                print(verdict.l3_question)
            return verdict

    # Check learned safe patterns
    for pattern, reason, reference in _LEARNED_SAFE:
        if re.search(pattern, text):
            verdict = L3Verdict(
                transform_name=transform_name,
                verdict="SAFE",
                reason=f"[learned] {reason}",
                reference=reference,
                confidence="medium",
            )
            if verbose:
                print(verdict.l3_question)
            return verdict

    # Unknown: no pattern matched — escalate to human
    verdict = L3Verdict(
        transform_name=transform_name,
        verdict="UNKNOWN",
        reason="No matching rule in L3 knowledge base. Human review required.",
        confidence="low",
    )
    if verbose:
        print(verdict.l3_question)
    return verdict


# ---------------------------------------------------------------------------
# Batch check: process all candidates from L2 output
# ---------------------------------------------------------------------------

def batch_check(candidates: list[dict], verbose: bool = True) -> list[L3Verdict]:
    """
    Run L3 check on all L2 candidates.

    Args:
        candidates: List of dicts with at least {"name": str} key
                    (matches the JSON format from run_experiment.py)

    Returns:
        List of L3Verdict, one per candidate
    """
    verdicts = []
    if verbose:
        print("=" * 60)
        print("L3 MONITOR - Self-Referential Safety Check")
        print("=" * 60)

    for c in candidates:
        name = c.get("name", c.get("transform_name", "unknown"))
        desc = c.get("description", "")
        v = check(name, description=desc, verbose=verbose)
        verdicts.append(v)

    if verbose:
        safe = [v for v in verdicts if v.is_safe]
        unsafe = [v for v in verdicts if v.verdict == "UNSAFE"]
        unknown = [v for v in verdicts if v.verdict == "UNKNOWN"]
        print("\n" + "=" * 60)
        print(f"SUMMARY: {len(safe)} SAFE, {len(unsafe)} UNSAFE, {len(unknown)} UNKNOWN")
        for v in safe:
            print(f"  [SAFE]    {v.transform_name}")
        for v in unsafe:
            print(f"  [UNSAFE]  {v.transform_name}")
        for v in unknown:
            print(f"  [UNKNOWN] {v.transform_name} -- needs human review")

    return verdicts


# ---------------------------------------------------------------------------
# Log writer
# ---------------------------------------------------------------------------

def append_to_log(verdict: L3Verdict, log_path: str) -> None:
    """Append a verdict to the l3_log.md file."""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n" + verdict.log_entry + "\n---\n")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import json as _json

    if len(sys.argv) < 2:
        print("Usage: python l3_monitor.py <transform_name> [description]")
        print("       python l3_monitor.py --batch <results_json>")
        print("       python l3_monitor.py --learn <name> SAFE|UNSAFE \"<reason>\" [reference]")
        print("       python l3_monitor.py --show-learned")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        with open(sys.argv[2]) as f:
            data = _json.load(f)
        candidates = data.get("candidates", [])
        verdicts = batch_check(candidates)

    elif sys.argv[1] == "--learn":
        if len(sys.argv) < 5:
            print("Usage: python l3_monitor.py --learn <name> SAFE|UNSAFE \"<reason>\" [reference]")
            sys.exit(1)
        name = sys.argv[2]
        human_verdict = sys.argv[3]
        reason = sys.argv[4]
        ref = sys.argv[5] if len(sys.argv) > 5 else ""
        rule = learn_from_feedback(name, human_verdict, reason, reference=ref)
        print(f"Learned new {human_verdict} rule:")
        print(f"  Pattern: {rule['pattern']}")
        print(f"  Reason: {rule['reason']}")
        print(f"  Keywords: {rule['keywords']}")
        # Verify: re-check the same transform
        print(f"\nVerification - re-checking '{name}':")
        v = check(name, verbose=False)
        print(f"  Verdict: {v.verdict} ({v.confidence} confidence)")
        print(f"  Reason: {v.reason}")

    elif sys.argv[1] == "--show-learned":
        if os.path.exists(_LEARNED_RULES_PATH):
            with open(_LEARNED_RULES_PATH, "r", encoding="utf-8") as f:
                data = _json.load(f)
            print("Learned UNSAFE rules:")
            for r in data.get("unsafe", []):
                print(f"  [{r['learned_at'][:10]}] /{r['pattern']}/ - {r['reason'][:60]}")
            print(f"\nLearned SAFE rules:")
            for r in data.get("safe", []):
                print(f"  [{r['learned_at'][:10]}] /{r['pattern']}/ - {r['reason'][:60]}")
            total = len(data.get("unsafe", [])) + len(data.get("safe", []))
            print(f"\nTotal learned rules: {total}")
        else:
            print("No learned rules yet.")

    else:
        name = sys.argv[1]
        desc = sys.argv[2] if len(sys.argv) > 2 else ""
        verdict = check(name, description=desc)
        print(verdict.log_entry)

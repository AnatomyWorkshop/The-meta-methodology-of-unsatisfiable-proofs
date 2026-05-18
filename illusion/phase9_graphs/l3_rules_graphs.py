"""
L3 Rules for Phase 9: Graph theory domain.

Based on Courcelle's theorem and treewidth complexity results.
Core question: "Can a bounded-treewidth algorithm decide property P?"
"""

import sys
import os

_phase9_dir = os.path.abspath(os.path.dirname(__file__))
_phase2_dir = os.path.abspath(os.path.join(_phase9_dir, '..', 'phase2_circuit'))
if _phase2_dir not in sys.path:
    sys.path.insert(0, _phase2_dir)

import l3_monitor


GRAPH_SAFE_PATTERNS = [
    (r"edge_addition", "SAFE", "high",
     "Adding random edges may increase treewidth beyond bound; deciding whether "
     "treewidth increased is NP-hard for general graphs (Arnborg et al. 1987). "
     "The induced property 'did the graph exceed tw=k?' requires computing treewidth, "
     "which is not decidable within the bounded-tw model itself.",
     "Arnborg, Corneil, Proskurowski 1987"),
    (r"treewidth_expansion", "SAFE", "high",
     "Targeted edge addition to increase treewidth. Verifying that treewidth increased "
     "beyond k requires solving an NP-hard problem (for general k). The bounded-tw "
     "algorithm cannot self-diagnose whether its own capacity has been exceeded.",
     "Arnborg et al. 1987; Bodlaender 1996"),
    (r"clique_sum", "SAFE", "high",
     "Gluing a (k+1)-clique forces treewidth > k. Deciding whether a graph contains "
     "a (k+1)-clique as a substructure that increases treewidth requires computing "
     "treewidth of the result, which exceeds bounded-tw algorithmic capacity.",
     "Robertson & Seymour 1986; Courcelle 1990"),
]

GRAPH_UNSAFE_PATTERNS = [
    (r"identity", "UNSAFE", "high",
     "No structural change. Trivially decidable.",
     "—"),
    (r"vertex_subdivision", "UNSAFE", "high",
     "Vertex subdivision preserves treewidth (tw(G') <= tw(G) for subdivisions). "
     "The operation is local and MSO2-definable. Deciding whether a graph was "
     "subdivided is decidable in linear time on bounded-tw graphs by Courcelle's theorem.",
     "Courcelle 1990"),
    (r"edge_contraction", "UNSAFE", "high",
     "Edge contraction can only decrease treewidth (tw(G/e) <= tw(G)). "
     "The operation is local and its effect on graph properties is decidable "
     "within the bounded-tw model.",
     "Courcelle 1990; Robertson & Seymour 1986"),
    (r"random_subgraph", "UNSAFE", "high",
     "Subgraph of a tw<=k graph has tw<=k. Edge deletion is a local operation "
     "whose effect on any MSO2 property is decidable in linear time on bounded-tw graphs.",
     "Courcelle 1990"),
    (r"planar_projection", "UNSAFE", "high",
     "Planarity testing is O(n) (Hopcroft-Tarjan 1974). Planar graphs have "
     "treewidth O(sqrt(n)). The projection operation and its effect on graph "
     "properties are decidable within the bounded-tw model.",
     "Hopcroft & Tarjan 1974; Courcelle 1990"),
]

GRAPH_UNKNOWN_PATTERNS = [
    (r"minor_embedding", "UNKNOWN", "medium",
     "Whether a specific minor (e.g., K5) is present is decidable in O(n^3) by "
     "Robertson-Seymour, but whether the INDUCED PROPERTY 'does embedding this minor "
     "change the graph's decidability regime?' is decidable within bounded-tw algorithms "
     "is related to open questions about the fine structure of the graph minor hierarchy. "
     "The relationship between minor structure and treewidth transitions is not fully "
     "characterized for all minor types.",
     "Robertson & Seymour 1986-2004; open"),
]


def inject_graph_rules():
    """Inject graph-theory-specific rules into the shared L3 monitor."""
    for pattern, verdict, confidence, reason, reference in GRAPH_SAFE_PATTERNS:
        l3_monitor._SAFE_PATTERNS.append((pattern, reason, reference))

    for pattern, verdict, confidence, reason, reference in GRAPH_UNSAFE_PATTERNS:
        l3_monitor._UNSAFE_PATTERNS.append((pattern, reason))

    for pattern, verdict, confidence, reason, reference in GRAPH_UNKNOWN_PATTERNS:
        if not hasattr(l3_monitor, '_UNKNOWN_PATTERNS'):
            l3_monitor._UNKNOWN_PATTERNS = []
        l3_monitor._UNKNOWN_PATTERNS.append((pattern, reason, reference))

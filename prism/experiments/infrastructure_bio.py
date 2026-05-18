"""
Prism on infrastructure and biological networks.

1. Power Grid (IEEE 14-bus, 30-bus, 118-bus test systems)
   - Nodes = buses (generators, loads, transformers)
   - Edges = transmission lines
   - Question: which buses contribute most to structural fragility?
   - Application: grid vulnerability assessment without power flow simulation

2. Drug-Drug Interaction Network
   - Nodes = drugs
   - Edges = known interactions (from synthetic model of real DDI patterns)
   - Question: which drug combinations break structural self-consistency?
   - Application: polypharmacy safety screening

For both: compute defect, per-node decomposition, identify fault lines.
"""

import numpy as np
import networkx as nx
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def laplacian(A):
    return np.diag(A.sum(axis=1)) - A


def fiedler_P(L):
    n = L.shape[0]
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    order = np.argsort(fiedler)
    perm = np.zeros(n, dtype=int)
    for rank, node in enumerate(order):
        perm[node] = order[n - 1 - rank]
    P = np.zeros((n, n))
    for i in range(n):
        P[i, perm[i]] = 1.0
    return (P + P.T) / 2


def duality_defect(L, P):
    comm = L @ P - P @ L
    return np.linalg.norm(comm, 'fro') / (np.linalg.norm(L, 'fro') + 1e-10)


def per_node_defect(L, P):
    comm = L @ P - P @ L
    L_norm = np.linalg.norm(L, 'fro') + 1e-10
    return np.linalg.norm(comm, axis=1) / L_norm


def analyze_graph(G, name, node_labels=None):
    """Full Prism analysis on a graph."""
    nodelist = list(G.nodes())
    n = len(nodelist)
    A = nx.to_numpy_array(G, nodelist=nodelist)
    L = laplacian(A)
    P = fiedler_P(L)

    delta = duality_defect(L, P)
    node_d = per_node_defect(L, P)

    print(f"\n{'='*65}")
    print(f"{name}")
    print(f"{'='*65}")
    print(f"  Nodes: {n}, Edges: {G.number_of_edges()}")
    print(f"  Density: {nx.density(G):.4f}")
    print(f"  Global duality defect: {delta:.4f}")
    print(f"  Interpretation: {'fragile' if delta > 0.4 else 'moderate' if delta > 0.2 else 'stable'}")

    # Top contributors
    order = np.argsort(node_d)[::-1]
    total = node_d.sum()
    print(f"\n  Top 10 defect contributors:")
    print(f"  {'Rank':<5} {'Node':<20} {'Defect':>8} {'% total':>8}")
    print(f"  {'-'*45}")
    for rank in range(min(10, n)):
        idx = order[rank]
        label = node_labels[idx] if node_labels else str(nodelist[idx])
        pct = node_d[idx] / total * 100
        print(f"  {rank+1:<5} {label:<20} {node_d[idx]:>8.4f} {pct:>7.1f}%")

    # Fiedler partition
    _, evecs = np.linalg.eigh(L)
    fiedler = evecs[:, 1]
    partition = (fiedler >= 0).astype(int)
    c0 = [nodelist[i] for i in range(n) if partition[i] == 0]
    c1 = [nodelist[i] for i in range(n) if partition[i] == 1]
    print(f"\n  Fiedler partition: {len(c0)} / {len(c1)} nodes")

    # Fault line: edges between partitions with highest defect nodes
    cross_edges = [(u, v) for u, v in G.edges()
                   if partition[nodelist.index(u)] != partition[nodelist.index(v)]]
    print(f"  Cross-partition edges: {len(cross_edges)} / {G.number_of_edges()} "
          f"({len(cross_edges)/G.number_of_edges()*100:.0f}%)")

    return delta, node_d


# ── IEEE Power Grid Test Systems ──────────────────────────────────────────────

def build_ieee14():
    """IEEE 14-bus test system (simplified topology)."""
    G = nx.Graph()
    # Bus types: G=generator, L=load, T=transformer
    buses = {
        1: "Gen-1 (slack)", 2: "Gen-2", 3: "Load-3", 4: "Load-4",
        5: "Load-5", 6: "Gen-6", 7: "Xfmr-7", 8: "Gen-8",
        9: "Load-9", 10: "Load-10", 11: "Load-11", 12: "Load-12",
        13: "Load-13", 14: "Load-14"
    }
    edges = [
        (1,2), (1,5), (2,3), (2,4), (2,5), (3,4), (4,5),
        (4,7), (4,9), (5,6), (6,11), (6,12), (6,13),
        (7,8), (7,9), (9,10), (9,14), (10,11), (12,13), (13,14)
    ]
    G.add_nodes_from(buses.keys())
    G.add_edges_from(edges)
    return G, buses


def build_ieee30():
    """IEEE 30-bus test system (simplified topology)."""
    G = nx.Graph()
    buses = {i: f"Bus-{i}" for i in range(1, 31)}
    buses[1] = "Gen-1 (slack)"
    buses[2] = "Gen-2"
    buses[5] = "Gen-5"
    buses[8] = "Gen-8"
    buses[11] = "Gen-11"
    buses[13] = "Gen-13"
    edges = [
        (1,2), (1,3), (2,4), (3,4), (2,5), (2,6), (4,6), (5,7),
        (6,7), (6,8), (6,9), (6,10), (9,11), (9,10), (4,12), (12,13),
        (12,14), (12,15), (12,16), (14,15), (16,17), (15,18), (18,19),
        (19,20), (10,20), (10,17), (10,21), (10,22), (21,22), (15,23),
        (22,24), (23,24), (24,25), (25,26), (25,27), (28,27), (27,29),
        (27,30), (29,30), (8,28), (6,28)
    ]
    G.add_nodes_from(buses.keys())
    G.add_edges_from(edges)
    return G, buses


def build_ieee118():
    """IEEE 118-bus approximation using a structured random graph."""
    # Real 118-bus has 118 nodes, 186 edges. We approximate the topology
    # using a power-law cluster graph (similar degree distribution).
    rng = np.random.default_rng(42)
    G = nx.powerlaw_cluster_graph(118, 3, 0.3, seed=42)
    buses = {i: f"Bus-{i}" for i in range(118)}
    # Mark some as generators
    gens = rng.choice(118, 19, replace=False)
    for g in gens:
        buses[g] = f"Gen-{g}"
    return G, buses


# ── Drug-Drug Interaction Network ─────────────────────────────────────────────

def build_ddi_network():
    """
    Synthetic drug-drug interaction network modeled on real DDI patterns.

    Structure:
    - 5 drug classes (antihypertensives, anticoagulants, antidepressants,
      statins, antibiotics), 8 drugs each = 40 drugs
    - Within-class interactions: moderate (drugs in same class often interact)
    - Cross-class interactions: sparse but some are dangerous
    - Known dangerous pairs: anticoagulants + antibiotics, etc.
    """
    rng = np.random.default_rng(123)

    classes = {
        "Antihypertensive": ["Lisinopril", "Amlodipine", "Losartan",
                             "Metoprolol", "Valsartan", "Hydrochlorothiazide",
                             "Enalapril", "Diltiazem"],
        "Anticoagulant":    ["Warfarin", "Heparin", "Rivaroxaban",
                             "Apixaban", "Dabigatran", "Enoxaparin",
                             "Clopidogrel", "Aspirin"],
        "Antidepressant":   ["Sertraline", "Fluoxetine", "Escitalopram",
                             "Venlafaxine", "Duloxetine", "Bupropion",
                             "Mirtazapine", "Amitriptyline"],
        "Statin":           ["Atorvastatin", "Rosuvastatin", "Simvastatin",
                             "Pravastatin", "Lovastatin", "Fluvastatin",
                             "Pitavastatin", "Ezetimibe"],
        "Antibiotic":       ["Amoxicillin", "Azithromycin", "Ciprofloxacin",
                             "Metronidazole", "Doxycycline", "Trimethoprim",
                             "Clarithromycin", "Erythromycin"],
    }

    all_drugs = []
    drug_class = {}
    for cls, drugs in classes.items():
        for d in drugs:
            all_drugs.append(d)
            drug_class[d] = cls

    n = len(all_drugs)
    G = nx.Graph()
    G.add_nodes_from(all_drugs)

    # Within-class interactions (moderate probability)
    for cls, drugs in classes.items():
        for i in range(len(drugs)):
            for j in range(i+1, len(drugs)):
                if rng.random() < 0.4:
                    G.add_edge(drugs[i], drugs[j], weight=1.0)

    # Cross-class interactions (sparse)
    class_list = list(classes.keys())
    for i in range(len(class_list)):
        for j in range(i+1, len(class_list)):
            drugs_i = classes[class_list[i]]
            drugs_j = classes[class_list[j]]
            # Base cross-class probability
            p = 0.05
            # Dangerous combinations have higher interaction rate
            if set([class_list[i], class_list[j]]) == {"Anticoagulant", "Antibiotic"}:
                p = 0.35
            elif set([class_list[i], class_list[j]]) == {"Antidepressant", "Anticoagulant"}:
                p = 0.25
            elif set([class_list[i], class_list[j]]) == {"Statin", "Antibiotic"}:
                p = 0.20

            for di in drugs_i:
                for dj in drugs_j:
                    if rng.random() < p:
                        G.add_edge(di, dj, weight=1.0)

    return G, all_drugs, drug_class


# ── Main ──────────────────────────────────────────────────────────────────────

def run_all():
    print()
    print("Prism Infrastructure & Biological Network Analysis")
    print()

    # ── Power Grids ───────────────────────────────────────────────────────
    print("\n" + "#"*65)
    print("# POWER GRID ANALYSIS")
    print("#"*65)

    G14, buses14 = build_ieee14()
    labels14 = [buses14[n] for n in G14.nodes()]
    d14, nd14 = analyze_graph(G14, "IEEE 14-Bus Power System", labels14)

    G30, buses30 = build_ieee30()
    labels30 = [buses30[n] for n in G30.nodes()]
    d30, nd30 = analyze_graph(G30, "IEEE 30-Bus Power System", labels30)

    G118, buses118 = build_ieee118()
    labels118 = [buses118[n] for n in G118.nodes()]
    d118, nd118 = analyze_graph(G118, "IEEE 118-Bus Power System (approx)", labels118)

    print(f"\n\n  Power Grid Summary:")
    print(f"  {'System':<30} {'Nodes':>6} {'Edges':>6} {'Defect':>8}")
    print(f"  {'-'*55}")
    print(f"  {'IEEE 14-bus':<30} {14:>6} {G14.number_of_edges():>6} {d14:>8.4f}")
    print(f"  {'IEEE 30-bus':<30} {30:>6} {G30.number_of_edges():>6} {d30:>8.4f}")
    print(f"  {'IEEE 118-bus (approx)':<30} {118:>6} {G118.number_of_edges():>6} {d118:>8.4f}")

    # ── Drug-Drug Interaction ─────────────────────────────────────────────
    print("\n\n" + "#"*65)
    print("# DRUG-DRUG INTERACTION NETWORK")
    print("#"*65)

    G_ddi, all_drugs, drug_class = build_ddi_network()
    labels_ddi = all_drugs
    d_ddi, nd_ddi = analyze_graph(G_ddi, "Drug-Drug Interaction Network (40 drugs, 5 classes)",
                                   labels_ddi)

    # Class-level analysis
    class_defect = {}
    for d_name, d_val in zip(all_drugs, nd_ddi):
        cls = drug_class[d_name]
        class_defect[cls] = class_defect.get(cls, 0) + d_val

    total = sum(class_defect.values())
    print(f"\n  Defect by drug class:")
    print(f"  {'Class':<20} {'Defect contrib':>14} {'% total':>8}")
    print(f"  {'-'*45}")
    for cls, v in sorted(class_defect.items(), key=lambda x: -x[1]):
        print(f"  {cls:<20} {v:>14.4f} {v/total*100:>7.1f}%")

    # Identify most structurally disruptive drug pairs
    print(f"\n  Most structurally disruptive drugs (top defect contributors):")
    print(f"  These drugs, when present in a polypharmacy regimen, contribute")
    print(f"  most to structural inconsistency of the interaction network.")

    # ── Stress test: remove high-defect nodes ─────────────────────────────
    print(f"\n\n{'='*65}")
    print("Stress Test: Effect of Removing High-Defect Nodes")
    print(f"{'='*65}")

    # Power grid: what happens if we remove the most vulnerable bus?
    print(f"\n  IEEE 30-bus: removing top defect contributor...")
    top_bus = list(G30.nodes())[np.argmax(nd30)]
    G30_reduced = G30.copy()
    G30_reduced.remove_node(top_bus)
    if nx.is_connected(G30_reduced):
        A_r = nx.to_numpy_array(G30_reduced)
        L_r = laplacian(A_r)
        P_r = fiedler_P(L_r)
        d_r = duality_defect(L_r, P_r)
        print(f"    Removed: {buses30[top_bus]}")
        print(f"    Defect before: {d30:.4f}")
        print(f"    Defect after:  {d_r:.4f}")
        print(f"    Change:        {d_r - d30:+.4f} ({'improved' if d_r < d30 else 'worsened'})")
    else:
        print(f"    Removed: {buses30[top_bus]} -- graph disconnected!")
        print(f"    This node is a critical bridge in the power grid.")

    # DDI: what happens if we remove the most disruptive drug?
    print(f"\n  DDI network: removing top defect contributor...")
    top_drug_idx = np.argmax(nd_ddi)
    top_drug = all_drugs[top_drug_idx]
    G_ddi_reduced = G_ddi.copy()
    G_ddi_reduced.remove_node(top_drug)
    if nx.is_connected(G_ddi_reduced):
        A_r = nx.to_numpy_array(G_ddi_reduced)
        L_r = laplacian(A_r)
        P_r = fiedler_P(L_r)
        d_r = duality_defect(L_r, P_r)
        print(f"    Removed: {top_drug} ({drug_class[top_drug]})")
        print(f"    Defect before: {d_ddi:.4f}")
        print(f"    Defect after:  {d_r:.4f}")
        print(f"    Change:        {d_r - d_ddi:+.4f} ({'improved' if d_r < d_ddi else 'worsened'})")
    else:
        components = list(nx.connected_components(G_ddi_reduced))
        largest = max(components, key=len)
        G_sub = G_ddi_reduced.subgraph(largest)
        A_r = nx.to_numpy_array(G_sub)
        L_r = laplacian(A_r)
        P_r = fiedler_P(L_r)
        d_r = duality_defect(L_r, P_r)
        print(f"    Removed: {top_drug} ({drug_class[top_drug]})")
        print(f"    Graph split into {len(components)} components")
        print(f"    Largest component defect: {d_r:.4f} (was {d_ddi:.4f})")


if __name__ == "__main__":
    run_all()

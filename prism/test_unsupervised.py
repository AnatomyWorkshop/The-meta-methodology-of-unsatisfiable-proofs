"""
Test unsupervised Prism on Karate Club.
Compares: baseline, supervised Prism (Fiedler P), unsupervised Prism (joint opt).
Also tests noise robustness of unsupervised mode.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from prism.unsupervised import unsupervised_prism, fiedler_clustering
from prism.core import learned_parity_operator, optimize_with_P

KARATE_EDGES = [
    (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,10),(0,11),
    (0,12),(0,13),(0,17),(0,19),(0,21),(0,31),(1,2),(1,3),(1,7),(1,13),
    (1,17),(1,19),(1,21),(1,30),(2,3),(2,7),(2,8),(2,9),(2,13),(2,27),
    (2,28),(2,32),(3,7),(3,12),(3,13),(4,6),(4,10),(5,6),(5,10),(5,16),
    (6,16),(8,30),(8,32),(8,33),(9,33),(13,33),(14,32),(14,33),(15,32),
    (15,33),(18,32),(18,33),(19,33),(20,32),(20,33),(22,32),(22,33),
    (23,25),(23,27),(23,29),(23,32),(23,33),(24,25),(24,27),(24,31),
    (25,31),(26,29),(26,33),(27,33),(28,31),(28,33),(29,32),(29,33),
    (30,32),(30,33),(31,32),(31,33),(32,33)
]
KARATE_TRUTH = [
    0,0,0,0,0,0,0,0,0,1, 0,0,0,0,1,1,0,0,1,0,
    1,0,1,1,1,1,1,1,1,1, 1,1,1,1
]

def build(n, edges):
    A = np.zeros((n,n))
    for u,v in edges: A[u,v]=A[v,u]=1.0
    return A

def laplacian(A):
    return np.diag(A.sum(1)) - A

def accuracy(pred, truth):
    t = np.array(truth)
    return max(np.mean(pred==t), np.mean(1-pred==t))

def add_noise(A, rate, rng):
    n = A.shape[0]; B = A.copy()
    for i in range(n):
        for j in range(i+1,n):
            if rng.random() < rate:
                B[i,j]=B[j,i]=1-B[i,j]
    return B

# ── Clean graph test ──────────────────────────────────────────────────────────
print("="*60)
print("Test 1: Clean Karate Club")
print("="*60)

n = 34
A_clean = build(n, KARATE_EDGES)
L_clean = laplacian(A_clean)

# Baseline
acc_base = accuracy(fiedler_clustering(L_clean), KARATE_TRUTH)

# Supervised (Fiedler P from same graph — best case)
P_sup = learned_parity_operator(L_clean)
res_sup = optimize_with_P(L_clean, P_sup)
acc_sup = accuracy(fiedler_clustering(res_sup.constrained_matrix), KARATE_TRUTH)

# Unsupervised
print("\nUnsupervised optimization:")
res_uns = unsupervised_prism(A_clean, n_outer=20, verbose=True)
acc_uns = accuracy(res_uns.community_labels, KARATE_TRUTH)

print(f"\n{'Method':<30} {'Accuracy':>10}")
print("-"*42)
print(f"{'Baseline':<30} {acc_base:>10.1%}")
print(f"{'Supervised (Fiedler P)':<30} {acc_sup:>10.1%}")
print(f"{'Unsupervised (joint opt)':<30} {acc_uns:>10.1%}")
print(f"\nUnsupervised duality defect: {res_uns.duality_defect_final:.6f}")
print(f"Unsupervised RMSE: {res_uns.rmse:.4f}")

# ── Noise robustness test ─────────────────────────────────────────────────────
print("\n"+"="*60)
print("Test 2: Noise Robustness (20 trials per level)")
print("="*60)

noise_levels = [0.0, 0.05, 0.10, 0.20]
n_trials = 20
rng = np.random.default_rng(42)

print(f"\n{'Noise':>7}  {'Baseline':>10}  {'Supervised':>12}  {'Unsupervised':>14}")
print("-"*50)

for noise in noise_levels:
    accs_b, accs_s, accs_u = [], [], []
    for _ in range(n_trials):
        A_n = add_noise(A_clean, noise, rng)
        L_n = laplacian(A_n)

        accs_b.append(accuracy(fiedler_clustering(L_n), KARATE_TRUTH))

        res_s = optimize_with_P(L_n, P_sup)
        accs_s.append(accuracy(fiedler_clustering(res_s.constrained_matrix), KARATE_TRUTH))

        res_u = unsupervised_prism(A_n, n_outer=15, verbose=False)
        accs_u.append(accuracy(res_u.community_labels, KARATE_TRUTH))

    print(f"{noise:>6.0%}  {np.mean(accs_b):>10.1%}  {np.mean(accs_s):>12.1%}  {np.mean(accs_u):>14.1%}")

print()
print("Supervised = Fiedler P learned from CLEAN graph (has prior knowledge)")
print("Unsupervised = P learned from NOISY graph itself (no prior knowledge)")

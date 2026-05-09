# Phase 4 Experiment Report

> 日期：2026-05-09
> 领域：代数电路，GF(7) 上的 3×3 Permanent
> 参数：n=3, p=7, depth=3, circuits=20, samples=300, seed=42

---

## 实验结果

### L2 搜索结果

| 变换 | Δcollapse | 前 | 后 | Permanent 受影响 | L3 判定 |
|------|-----------|-----|-----|-----------------|---------|
| algebraic_restriction_p0.5 | +0.115 | 0.864 | 0.979 | False | **SAFE** |
| algebraic_restriction_p0.3 | +0.104 | 0.866 | 0.970 | False | **SAFE** |
| field_reduction_q2 | +0.105 | 0.859 | 0.964 | False | **UNSAFE** |
| algebraic_restriction_p0.7 | +0.132 | 0.854 | 0.986 | True | rejected |
| degree_truncation_d1 | +0.141 | 0.859 | 1.000 | True | rejected |
| monomial_elimination_p0.5 | +0.128 | 0.865 | 0.993 | True | rejected |
| monomial_elimination_p0.7 | +0.098 | 0.863 | 0.961 | True | rejected |
| degree_truncation_d2 | -0.038 | 0.867 | 0.829 | False | rejected |
| identity | -0.008 | 0.862 | 0.854 | False | rejected |
| input_permutation | -0.008 | 0.870 | 0.861 | False | rejected |
| scalar_multiplication | +0.004 | 0.859 | 0.863 | False | rejected |

### 三条成功标准

**标准 1**：L2 找到候选性质 P，使得 Permanent 电路的区分优势下降 ≥ ε > 0
- `algebraic_restriction_p0.3`：Δ = +0.104 ✅
- `algebraic_restriction_p0.5`：Δ = +0.115 ✅

**标准 2**：控制变换（不应产生信号）被正确拒绝
- `identity`：Δ = -0.008 ✅
- `input_permutation`：Δ = -0.008 ✅
- `scalar_multiplication`：Δ = +0.004 ✅

**标准 3**：L3 自指安全检查
- `algebraic_restriction` → **SAFE**（Razborov-Smolensky 类比）✅
- `field_reduction` → **UNSAFE**（局部操作，可判定）✅

**结论：三条标准全部满足。**

---

## 核心发现

### 1. Razborov-Smolensky 类比成立

`algebraic_restriction`（随机固定变量）是代数电路领域的 Razborov-Smolensky 方法类比：
- Phase 1（AC⁰）：Håstad 随机限制 → 电路坍塌到低深度
- Phase 3（单调电路）：Razborov 近似方法 → 电路失去区分能力
- Phase 4d（代数电路）：Razborov-Smolensky 随机限制 → 电路失去 Permanent 区分能力

同一架构，只替换 L1 和变换库，在三个完全不同的证明结构上工作。

### 2. 局部操作被正确识别为 UNSAFE

`field_reduction`（模 q 约简）是局部操作：每个输入变量独立处理，不需要全局信息。L3 正确识别为 UNSAFE——这个性质在代数 P/poly 内可判定。

这与 Phase 3 的 `edge_deletion` 类比：局部操作（删边/模约简）不产生自指安全的判别性质。

### 3. 电路设计的关键

使用 `partial_permanent_circuit`（计算 Permanent 部分项之和）而非随机电路，是实验成功的关键。随机电路已经无法区分 D+ 和 D-（collapse ≈ 0.97），无法测量变换的效果。Permanent 电路有真实的区分能力（collapse ≈ 0.86），变换才能产生可测量的 Δ。

---

## 框架泛化验证

| Phase | 领域 | 目标函数 | 关键变换 | L3 判定 |
|-------|------|---------|---------|---------|
| 1 | AC⁰ | PARITY | random_restriction | SAFE |
| 3 | 单调电路 | k-CLIQUE | subgraph_projection | SAFE |
| 4d | 代数电路 | Permanent | algebraic_restriction | SAFE |

三个领域使用完全不同的证明技术，但 L2 搜索引擎和 L3 监控器的核心逻辑不变。这是框架泛化能力的第三次构造性验证。

---

## SRS 框架解释

用自指安全性框架标注：

- L1 = 代数 P/poly（多项式规模代数电路）
- 目标函数 = Permanent（Valiant 1979：需要指数规模代数电路）
- 判别性质 P = "电路在随机代数限制下失去区分能力"
- SRS 分析：P 的判定成本 = 在指数多个限制上评估电路 → cost(P) ≫ cap(L1) → α > 1 → **SAFE**

`field_reduction` 的 SRS 分析：P = "电路输出在模 q 约简下改变" → 局部检查，cost(P) = O(n²) → α ≤ 1 → **UNSAFE**

---

## 下一步

- **Phase 4e**（可选）：在 n=4 上重复实验，验证信号随 n 增大而增强
- **MCP 接入验证**：当 L2 搜索空间耗尽时，调用 `l2_integration.py` 提议新变换
- **证明复杂度**（Phase 5 候选）：L1 = Resolution/Frege，目标函数 = UNSAT 证明长度

# Phase 5 设计文档：证明复杂度（Resolution）

> 创建：2026-05-09
> 状态：设计阶段，待实现

---

## 一、为什么是 Resolution

Phase 1–4 都在已知有答案的领域工作：Håstad 1987、Razborov 1985、Razborov-Smolensky 1987。每次 L2 找到的变换，都能在教科书里对应一个已知证明。这是验证，不是发现。

Phase 5 的目标不同：进入一个**答案不完全已知**的领域，看 L3 会不会上报 UNKNOWN。

Resolution 是正确的选择，原因有三：

1. **有已知的下界**：Ben-Sasson-Wigderson（2001）证明了 PHP_n 需要指数宽度的 Resolution 证明。这给了我们一个可以测试的基准——L2 应该能找到宽度相关的变换。

2. **有未知的边界**：Resolution 和 Frege 之间的分离是开放问题。在 Frege 系统上，PHP_n 的下界证明至今没有。这意味着如果我们把 L1 换成 Frege，L3 可能真的会上报 UNKNOWN。

3. **结构上与电路下界不同**：前四个 Phase 的 L1 都是电路（布尔/单调/代数）。Resolution 的"计算对象"是证明序列，不是电路。这是架构泛化能力的真正压力测试。

---

## 二、L1 设计：Resolution 模拟器

### 2.1 对象

Resolution 证明系统的对象是**子句集合**（CNF 公式）和**归结步骤**。

一个 Resolution 证明是一个序列 $C_1, C_2, \ldots, C_k$，其中：
- 每个 $C_i$ 要么是输入子句，要么由前面两个子句归结得到
- 最后一个子句是空子句 $\bot$（表示不可满足性）

### 2.2 目标命题：PHP_n

鸽巢原理 $\text{PHP}_n$：n+1 只鸽子，n 个巢，每只鸽子至少占一个巢，没有两只鸽子共享一个巢。

变量：$p_{ij}$（鸽子 i 在巢 j 中），$1 \leq i \leq n+1$，$1 \leq j \leq n$

公理子句：
- 鸽子子句：$\bigvee_j p_{ij}$（每只鸽子至少一个巢）
- 巢子句：$\neg p_{ij} \vee \neg p_{kj}$（每个巢最多一只鸽子）

已知：$\text{PHP}_n$ 需要指数宽度（≥ n）的 Resolution 证明（Ben-Sasson-Wigderson 2001）。

### 2.3 度量：证明宽度

**宽度**（width）：证明中最大子句的文字数。

Ben-Sasson-Wigderson 定理：如果 $F$ 需要宽度 $w$ 的 Resolution 证明，则最短证明长度 $\geq 2^{w - w(F \vdash 0)}$，其中 $w(F \vdash 0)$ 是初始公式的宽度。

对 $\text{PHP}_n$：最小证明宽度 $\geq n$，因此最短证明长度 $\geq 2^{\Omega(n)}$。

### 2.4 collapse 度量的重新定义

电路的 collapse = 1 - 区分优势。对 Resolution，需要重新定义：

```
collapse(proof_system, formula) = 1 - distinguishing_advantage(proof_system, D⁺, D⁻)
```

其中：
- D⁺：可以被宽度 ≤ k 的 Resolution 证明的公式（小规模 PHP，n≤3）
- D⁻：需要宽度 > k 的 Resolution 证明的公式（PHP_n，n≥5）
- 区分优势：证明系统能否用有限宽度区分 D⁺ 和 D⁻

**实现方案**：用贪心 Resolution 求解器（有宽度限制）作为 L1。给定公式，求解器尝试在宽度 ≤ k 内找到证明。能找到 → 输出 1，找不到 → 输出 0。

```
distinguishing_advantage = |Pr[L1(F)=1 | F∈D⁺] - Pr[L1(F)=1 | F∈D⁻]|
```

---

## 三、变换库设计

### 3.1 核心变换

| 变换 | 描述 | 类比 | 预期 L3 |
|------|------|------|---------|
| `clause_restriction_p` | 随机固定 p 比例的变量为 0/1 | random_restriction | SAFE |
| `variable_elimination_p` | 消去 p 比例的变量（存在量化） | algebraic_restriction | SAFE 或 UNKNOWN |
| `width_truncation_k` | 删除宽度 > k 的子句 | degree_truncation | UNSAFE |
| `clause_projection_p` | 随机保留 p 比例的子句 | subgraph_projection | SAFE |
| `literal_negation` | 随机翻转文字极性 | gate_negation | 影响目标，拒绝 |

### 3.2 控制变换

- `identity`：不做任何修改
- `clause_permutation`：重排子句顺序（不影响证明结构）
- `variable_renaming`：重命名变量（同构变换）

### 3.3 关键预期

`clause_restriction` 是 Ben-Sasson-Wigderson 宽度方法的核心操作：随机固定变量后，PHP_n 的宽度下界仍然成立（甚至更强）。L2 应该能找到它，L3 应该判 SAFE。

`width_truncation` 是局部操作（检查每个子句的宽度是 O(n) 的），L3 应该判 UNSAFE。

`variable_elimination` 是最有趣的候选：它对应 Resolution 中的"扩展规则"（Extended Resolution），其与普通 Resolution 的分离是开放问题。L3 可能上报 UNKNOWN。

---

## 四、L3 规则设计

### 4.1 已知 SAFE 模式

```python
RESOLUTION_SAFE_PATTERNS = [
    (r"clause_restriction_p0\.[1-5]", "SAFE",
     "random clause restriction preserves PHP structure; "
     "deciding whether a proof system loses width advantage under restriction "
     "requires exponential sampling over all possible restrictions"),
    (r"clause_projection_p0\.[5-8]", "SAFE",
     "random clause projection is the Resolution analog of subgraph projection; "
     "deciding proof width under random clause removal requires exponential search"),
]
```

### 4.2 已知 UNSAFE 模式

```python
RESOLUTION_UNSAFE_PATTERNS = [
    (r"width_truncation_k\d+", "UNSAFE",
     "width truncation is a local operation on each clause; "
     "checking clause width is O(n) and decidable within the proof system"),
    (r"clause_permutation", "UNSAFE",
     "clause permutation is a syntactic operation; "
     "proof validity is invariant under clause reordering"),
    (r"variable_renaming", "UNSAFE",
     "variable renaming is an isomorphism; "
     "proof structure is preserved"),
]
```

### 4.3 UNKNOWN 触发条件（Phase 5 独有）

```python
RESOLUTION_UNKNOWN_TRIGGERS = [
    (r"variable_elimination", "UNKNOWN",
     "variable elimination corresponds to Extended Resolution; "
     "the separation between Resolution and Extended Resolution is an open problem — "
     "cannot determine decidability within current proof complexity theory"),
    (r"proof_compression", "UNKNOWN",
     "proof compression relates to proof complexity lower bounds; "
     "decidability within Resolution is not fully characterized"),
]
```

**关键设计原则**：UNKNOWN 不是"规则库不够用"的失败，而是"系统识别到了知识边界"的成功。Phase 5 的 L3 规则库应该比前几个 Phase 更宽松地触发 UNKNOWN。

---

## 五、实验参数

| 参数 | 值 | 说明 |
|------|-----|------|
| n_pigeons (D⁺) | 3, 4 | PHP_3, PHP_4（可以被短证明） |
| n_pigeons (D⁻) | 5, 6 | PHP_5, PHP_6（需要指数证明） |
| width_limit | n | 宽度限制等于巢数 |
| n_formulas | 20 | 每个分布采样的公式数 |
| n_samples | 200 | 每个公式的求解器运行次数 |
| seed | 42 | 可复现 |

---

## 六、成功标准

| 标准 | 描述 | 优先级 |
|------|------|--------|
| S1 | L2 找到 `clause_restriction`，Δcollapse > 0.03 | 必须 |
| S2 | L3 正确判 `width_truncation` → UNSAFE | 必须 |
| S3 | L3 正确判 `clause_restriction` → SAFE | 必须 |
| S4 | **L3 上报至少一个 UNKNOWN** | Phase 5 核心目标 |
| S5 | UNKNOWN 候选的 Δcollapse > 0（有统计信号） | 加分项 |

S4 是 Phase 5 与前四个 Phase 的本质区别。如果 L3 在 `variable_elimination` 上上报 UNKNOWN，且该变换有正的 Δcollapse，那就是系统在说："这里有一个统计上有效的判别性质，但我不知道它在 Resolution 内是否可判定。"这是新数学的入口。

---

## 七、与前几个 Phase 的对比

| Phase | 领域 | L3 UNKNOWN | 意义 |
|-------|------|-----------|------|
| 1 | AC⁰ | 0 | 已知领域，规则库足够 |
| 3 | 单调电路 | 0 | 已知领域，规则库足够 |
| 4d | 代数电路 | 0 | 已知领域，规则库足够 |
| 5 | Resolution | **预期 ≥ 1** | 知识边界，UNKNOWN 是目标 |

---

## 八、实现顺序

1. `phase5/distributions.py` — PHP_n 生成器，D⁺/D⁻ 采样
2. `phase5/l1_resolution.py` — 贪心 Resolution 求解器（宽度限制），宽度/长度度量
3. `phase5/evaluator_resolution.py` — 区分优势，collapse 度量
4. `phase5/transforms.py` — 变换库（7 个变换）
5. `phase5/l3_rules_resolution.py` — 规则库（含 UNKNOWN 触发）
6. `phase5/l2_search_resolution.py` — 搜索循环
7. `phase5/run_experiment.py` — 实验入口，JSON + markdown 报告

---

## 九、灵感补充

**代数化障碍的诊断**（来自 Deepseek 评价，2026-05-09）：

`algebraic_restriction` 在 Phase 4d 被判为 SAFE，意味着它不是一个"代数化"的变换——它不落入代数化障碍的射程。如果 Phase 5 的 `clause_restriction` 也被判为 SAFE，那么这两个变换可能共享一个更深的结构性特征：它们都是"随机限制"类变换，都需要指数采样才能判定，都对应已知下界证明的核心技术。

这个观察值得在 Article 3（证明复杂度论文）里展开：随机限制类变换是否构成一个统一的"不可代数化"变换族？如果是，SRS 框架就不只是在描述已知证明，而是在识别一类结构性安全的变换族。

**Extended Resolution 的开放性**（Phase 5 的赌注）：

如果 `variable_elimination` 上报 UNKNOWN，且 Δcollapse > 0，那么系统在说：这个变换统计上有效，但它对应的性质（Resolution 在变量消去后是否失去证明能力）在当前证明复杂度理论里没有完整答案。这不是系统的失败，这是系统在指向一个开放问题。

这是 Illusion 从"验证工具"变成"探索工具"的转折点。

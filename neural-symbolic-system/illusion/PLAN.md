# Illusion — 分层自指安全原型系统

> 目录名 `illusion` 的含义：这个系统试图看见结构，但它看见的可能是幻象。
> 这不是示弱，而是最高级别的自反性诚实——apophenia 的对立面不是"不看"，而是"知道自己在看，并且能检验"。

---

## 一、这个系统是什么

**Illusion** 是一个最小可行原型，用于验证以下命题：

> 一个分层架构的搜索系统，如果其判别性质生成器（L2）被严格隔离于被分析模型（L1）之外，能否在不触发自指陷阱的情况下，自主发现对 L1 有效的判别性质？

这不是通用定理证明器。它是一个**概念验证实验**，目标是在 AC⁰ 这个已知有解的玩具领域里，让机器走到人类已经走过的那一步——然后问：它走的路和人类走的路，结构上是否相同？

---

## 二、名字候选

Deepseek 提供的候选，供参考：

| 名字 | 含义 | 适用阶段 |
|---|---|---|
| **Apophenia** | 在随机中识别模式的倾向；双刃——可能是真结构，可能是幻象 | 如果系统逼近 Level 3 |
| **Bastion** | 堡垒；L3 是堡垒，L2 是从堡垒向外探索的斥候 | 如果第一个实验跑通 |
| **Glymph** | glimpse + lymph；能看到自己是否会自噬的免疫视力 | 如果系统能自我监控 |
| **Metron** | 度量；SRS 指数的测量，方法论的城市基建 | 纯理论构想阶段 |
| **Orthos** | 正交分层；强调架构的正交性 | 纯理论构想阶段 |
| **Illusion** | 幻象；知道自己在看，并且能检验 | 当前目录名，已在使用 |

当前用 `illusion` 作为目录名。系统本身的名字待第一个实验结果出来后决定。

---

## 三、架构设计

### 三层结构（完整版）

```
L3 自反层（安全监控）
    ↕ 监控 L2 是否滑入 L1
L2 判别层（判别性质生成器，可进化）
    ↕ 分析 L1，生成候选性质 P
L1 对象层（被分析的目标模型）
```

| 层 | 功能 | 计算能力 | Phase 1 实现 |
|---|---|---|---|
| L1 | 被分析的目标模型 | 多项式时间（AC⁰） | AC⁰ 电路模拟器 |
| L2 | 生成候选判别性质 P | 严格强于 L1（指数级） | 变换规则搜索引擎 |
| L3 | 监控 P 是否滑入 L1 | 不可判定或超数学 | **Phase 1 由人类充当** |

### Phase 1 的关键简化

L3 在 Phase 1 由人类手动充当：检查 L2 找到的 P 是否能被 AC⁰ 电路判定。如果能，标记为"不安全路径"并丢弃。这不是偷懒——这是正确的实验设计。L3 的自动化是 Phase 2 的目标。

---

## 四、分阶段实现计划

### Phase 0：理论准备 — ✅ 已完成

**结果**：14 个案例，14 个安全（含 2 个隐式安全），0 个反例。跨越布尔电路、代数电路、通信复杂度、证明复杂度、数理逻辑五个领域。详见 `phase0-verification.md`。

**对框架的修正**：
- 隐式判别性质 Remark（Williams、McKay-Williams 的隐式 P）
- 量词敏感性条款（证明复杂度中局部 vs 全局 P 的区分）
- 两项修正均已写入论文 Ch.2 和 Ch.6

**判断**：理论地基稳固。框架定义已收敛。进入 Phase 1。

---

### Phase 1：两层玩具系统 — ✅ 完成

**目标**：在 AC⁰ 领域验证"L2 能自主发现自指安全的判别性质"。

**结果（2026-05-02）**：三条成功标准全部满足。详见 `phase1-results.md`。

| 变换 | Collapse Score | PARITY 受影响 | L3 判定 |
|---|---|---|---|
| random_restriction (p=0.3) | 0.948 | 否 | **SAFE** |
| random_restriction (p=0.5) | 0.905 | 否 | **SAFE** |
| random_restriction (p=0.7) | 0.834 | 否 | **SAFE** |
| input_permutation | 0.835 | 否 | **UNSAFE（假阳性）** |
| gate_substitution | 0.998 | 是 | 已拒绝（L2） |
| depth_reduction | 0.784 | 是 | 已拒绝（L2） |

**核心发现**：collapse score 是真实信号，但不足以区分真假阳性——L3 的自指安全检查是必要的，不是可选的。

**目录结构**：
```
illusion/
├── PLAN.md
├── l3_log.md               # 活的 L3 决策记录（append-only）
├── phase0-verification.md
├── phase1-results.md       # 实验报告 ✅
├── phase1/
│   ├── l1_circuit.py       # AC⁰ 电路模拟器
│   ├── l2_search.py        # 判别性质搜索引擎（含 collapse 度量）
│   ├── l3_monitor.py       # L3 规则库 + 自动检查器
│   ├── evaluator.py        # 错误率评估（蒙特卡洛）
│   ├── transforms.py       # 变换规则库（含压力测试变换）
│   ├── run_experiment.py   # 主实验脚本
│   └── results/            # 实验结果 JSON
```

---

### Phase 2：L3 自动化 — 🔄 规则库已实现，压力测试进行中

**目标**：把人工 L3 替换为自动检查器，并验证规则库的边界。

**已完成（2026-05-02）**：

`phase1/l3_monitor.py` 已实现。架构如下：

```
输入：transform_name + description（自然语言）
  ↓
正则模式匹配
  ├── UNSAFE 模式库（已知多项式时间可判定的性质类）
  │     permut / symmetr / invariant → 置换不变性，多项式时间
  │     monoton → 单调性，多项式时间
  │     linear → GF(2) 线性性，BLR 测试
  │     constant → 常数函数，AC⁰
  │     depth_reduc / gate_substit → 电路结构性质，AC⁰
  └── SAFE 模式库（已知超出 AC⁰ 的性质类）
        random_restrict → 随机限制坍塌，指数枚举，Håstad 1986
        approximat → 近似方法，Razborov 1985
        algebraic_degree → 代数次数，Razborov-Smolensky 1987
  ↓
输出：L3Verdict（verdict / reason / reference / confidence）
  + l3_question（结构化问题，供人类最小化审查）
  + log_entry（格式化日志条目，直接写入 l3_log.md）
```

**L3 的三种输出模式**：

1. **SAFE**：规则库命中，有文献支撑，高置信度 → 直接保留候选
2. **UNSAFE**：规则库命中，多项式时间可判定 → 直接丢弃
3. **UNKNOWN**：规则库未命中 → 生成结构化问题，升级到人类 L3

**人类 L3 的最小工作量设计**：

当 L3 输出 UNKNOWN 时，它生成一个标准化问题：

```
L3 CHECK: '<transform_name>'
  Question: Can an AC^0 circuit decide whether a function satisfies
            the property induced by this transform?
  AI diagnosis: UNKNOWN — No matching rule in L3 knowledge base.
  Confidence: low
  Your answer: YES (unsafe, discard) / NO (safe, keep) / OVERRIDE
```

你只需要回答 YES / NO / OVERRIDE + 一行理由。这个回答会被追加到 `l3_log.md`，并可以反向更新规则库（把新的模式加入 `_SAFE_PATTERNS` 或 `_UNSAFE_PATTERNS`）。

**L3 日志机制**：

所有 L3 决策记录在 `illusion/l3_log.md`。每条记录包含：
- 时间戳 + 候选名称
- AI 诊断（verdict + reason + reference）
- 人类决策（如果 AI 是 UNKNOWN 或人类 override）
- 事后验证（如果后来有新证据）

这个日志是活的：它记录的不只是"这个候选是否安全"，而是"我们是怎么知道它安全的"。这是框架的认识论记录，不是执行日志。

**Phase 2 验证结果（2026-05-03）**：

压力测试实验已运行（n=8/seed=42，n=12/seed=7）。结果：

| 实验 | exhaustive collapse | random_restriction collapse | L3 自动判定 |
|---|---|---|---|
| n=8, seed=42 | **1.000** | 0.879–0.969 | UNSAFE（正确） |
| n=12, seed=7 | **1.000** | 0.887–0.957 | UNSAFE（正确） |

关键观察：
- `exhaustive_parity_equivalent_check` 在两次实验中都以 collapse=1.000 排第一，成功通过 L2
- L3 规则库在两次实验中都正确将其标记为 UNSAFE（0 UNKNOWN）
- 模式在 n=8 → n=12 之间完全稳定
- `gate_substitution` 在 n=12 时 collapse=1.000 但 parity_affected=True，被 L2 正确过滤

**Phase 2 当前状态**：压力测试通过。L3 自动化在已知变换上准确率 100%。

**Phase 2 下一步**：
1. 扩展变换注册表（加入更多控制变换：identity、input_negation）
2. 设计 UNKNOWN 候选的学习循环（人类判断 → 规则库更新）
3. 开始 Phase 3 设计：单调电路 L1 + k-CLIQUE 目标函数

**输出文件**：
- `illusion/phase1/l3_monitor.py` — 规则库 + 检查器 + 日志写入器
- `illusion/l3_log.md` — 活的 L3 决策记录
- `illusion/phase1/results/` — 实验 JSON（含 seed，可复现）

---

### Phase 3：扩展到更强模型（未来）

**目标**：把同样的架构应用于单调电路（L1 = 单调 P/poly），看 L2 能否发现 Razborov 的近似方法。

这是 Phase 1 成功后的自然延伸。不需要现在规划细节。

---

## 五、技术选型建议

**语言**：Python（快速原型，丰富的组合搜索库）

**核心依赖**：
- 电路模拟：手写或用 `sympy` 的布尔代数
- 搜索：`itertools` 枚举 + 简单的启发式剪枝
- 评估：蒙特卡洛采样（随机输入上的错误率估计）

**不需要**：
- 神经网络（Phase 1 是符号搜索，不是学习）
- 大型定理证明器（Phase 1 的验证是手动的）
- GPU（规模很小）

---

## 六、成功的判断标准

Phase 1 成功 = 以下三条同时满足：

1. L2 在搜索空间里找到了一个候选性质 P，使得：对所有深度 ≤ d、规模 ≤ s 的 AC⁰ 电路，应用 P 后错误率 ≥ ε > 0
2. P 对 PARITY 无效（PARITY 不满足 P 的"坍塌"条件）
3. 手动 L3 检查：P 不能被 AC⁰ 电路判定（自指安全）

如果这三条都满足，我们就在玩具领域里证明了：分层搜索 + 自指安全检查，能产出与人类证明等价的结构性结果。

---

## 七、这个系统和论文的关系

这个原型不是论文的一部分。它是论文框架的**工程化检验**。

论文说：成功的下界证明必须使用自指安全的判别性质。
原型问：如果我们把这个条件硬连线进搜索架构，系统能否自主找到这样的性质？

如果原型成功，它为论文的第一定律提供了一个**构造性的支持**——不只是"已知证明都满足这个条件"，而是"按照这个条件设计的系统能重新发现这些证明"。

这是从归纳到演绎的一步。

---

## 八、之后的方向（Phase 3 之后）

Phase 1 和 Phase 2 完成后，Illusion 将成为一个可以自动发现并验证判别性质的系统。之后的工作方向：

### 接入 MCP 协议，扩充搜索空间

把 L2 的搜索空间从"手写变换规则"扩展到"AI 生成的候选性质"。通过 MCP 协议，L2 可以调用外部工具（定理证明器、符号计算引擎、文献检索）来生成和验证候选性质。L3 仍然是安全边界——任何 AI 生成的候选性质都必须通过 L3 的自指安全检查。

### 从 AC⁰ 到更强模型

Phase 3 已规划：把同样的架构应用于单调电路（L1 = 单调 P/poly），看 L2 能否发现 Razborov 的近似方法。之后可以扩展到：
- 代数电路（L1 = 代数 P/poly）
- 证明复杂度（L1 = Resolution/Frege）
- 形式系统（L1 = PA/ZFC 的可证明性）

### 从证明数学公式到 AI 进化最优路径

当 L2 的搜索空间足够大、L3 的自动化足够可靠时，这个架构可以用于：
- 在已知有解的数学领域，让系统重新发现已知证明（验证）
- 在未知领域，让系统提出候选判别性质，由人类 L3 评估（探索）
- 最终目标：系统能自主识别"这个问题在当前模型下不可满足"，并给出结构性原因

这不是通用 AI 数学家。这是一个专门用于发现不可满足性结构的工具。它的价值在于：在人类投入大量资源之前，告诉你某条路是死胡同。

---

*最后一句：*
*`illusion` 这个名字的意思不是"这是假的"。*
*它的意思是：我们知道自己可能在看幻象，所以我们设计了一个能检验自己是否在看幻象的系统。*
*这就是 L3 的存在意义。*

---
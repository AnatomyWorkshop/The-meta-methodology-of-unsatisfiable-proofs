# Illusion — 分层自指安全原型系统

> 目录名 `illusion` 的含义：这个系统试图看见结构，但它看见的可能是幻象。
> 这不是示弱，而是最高级别的自反性诚实——apophenia 的对立面不是"不看"，而是"知道自己在看，并且能检验"。

---

## 一、这个系统是什么

**Illusion** 是一个最小可行原型，用于验证以下命题：

> 一个分层架构的搜索系统，如果其判别性质生成器（L2）被严格隔离于被分析模型（L1）之外，能否在不触发自指陷阱的情况下，自主发现对 L1 有效的判别性质？

这不是通用定理证明器。它是一个**概念验证实验**，目标是在 AC⁰ 这个已知有解的玩具领域里，让机器走到人类已经走过的那一步——然后问：它走的路和人类走的路，结构上是否相同？

---

## 二、架构设计

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

## 三、分阶段实现计划

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

**核心发现**：collapse score 是真实信号，但不足以区分真假阳性——L3 的自指安全检查是必要的，不是可选的。

---

### Phase 2：L3 自动化 — ✅ 完成

**目标**：把人工 L3 替换为自动检查器，并验证规则库的边界。

**架构**：`phase1/l3_monitor.py` — 正则模式匹配 + UNKNOWN 学习循环。三种输出：SAFE（保留）、UNSAFE（丢弃）、UNKNOWN（升级到人类）。详见 `docs/phase2-report.md`。

**已完成**：
1. ✅ 规则库实现 + 压力测试通过（2026-05-02 ~ 05-03）：已知变换准确率 100%
2. ✅ 基线校准（2026-05-04）：identity collapse = 0.889，确认 ~0.89 基线偏差
3. ✅ UNKNOWN 学习循环（2026-05-04）：人类反馈 → 提取关键词 → 生成新规则 → 持久化
4. ✅ Δcollapse 实现（2026-05-04）：collapse_after - collapse_before，阈值 0.03。修正了全部已知假阳性，并发现 p=0.7 不产生有效坍塌（新发现）

---

### Phase 3：扩展到单调电路 — ✅ 完成

**目标**：把同样的架构应用于单调电路（L1 = 单调 P/poly），看 L2 能否发现 Razborov 的近似方法。

**结果（2026-05-04）**：泛化验证成功。详见 `docs/phase3-report.md`。

**核心发现**：
- L2 在 9 个变换中找到 2 个候选：`subgraph_projection_p0.7`（Δ=+0.245）和 `edge_deletion_p0.1`（Δ=+0.081）
- L3 正确分类：`subgraph_projection` → SAFE（Razborov 近似方法的类比），`edge_deletion` → UNSAFE（单调操作，可判定）
- 同一架构，只替换 L1 和变换库，在完全不同的证明结构上工作
- `distribution_switch`（纯分布切换）被 L2 正确拒绝（Δ=+0.004）——真正的信号来自修改输入空间的变换

**架构验证**：Phase 1（AC⁰/随机限制）和 Phase 3（单调/子图投影）使用完全不同的证明技术，但 L2 搜索引擎和 L3 监控器的核心逻辑不变。这是框架泛化能力的构造性证据。

---

## 四、技术选型建议

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

## 五、成功的判断标准

Phase 1 成功 = 以下三条同时满足：

1. L2 在搜索空间里找到了一个候选性质 P，使得：对所有深度 ≤ d、规模 ≤ s 的 AC⁰ 电路，应用 P 后错误率 ≥ ε > 0
2. P 对 PARITY 无效（PARITY 不满足 P 的"坍塌"条件）
3. 手动 L3 检查：P 不能被 AC⁰ 电路判定（自指安全）

如果这三条都满足，我们就在玩具领域里证明了：分层搜索 + 自指安全检查，能产出与人类证明等价的结构性结果。

---

## 六、这个系统和论文的关系

详见 `docs/paper-plan.md`。

核心定位：Illusion 是论文框架的工程化检验，不是论文的一部分。成功时为第一定律提供构造性支持。

当前节点：不要现在重写论文。Phase 2 完成后在 Ch.6 或附录加入 Illusion 实验。

---

## 七、人类与 AI 的分工（最高效工作流程）

**分工原则**：
- **你做 L3**：判断哪些候选性质是真正有价值的，哪些是假阳性。需要数学直觉和领域知识，AI 目前做不好。
- **AI 做 L2**：生成候选性质，枚举变换规则，评估 collapse score。机械性搜索，AI 比人快。
- **AI 做 L1**：模拟电路，计算错误率，生成测试用例。纯计算，AI 做。
- **你做方向决策**：决定下一个要探索的领域（AC⁰ → 单调电路 → 代数电路 → 证明复杂度）。

**标准工作循环（5 步）**：
1. 你指定一个新领域（"我们来试试单调电路"）
2. AI 实现 L1 模拟器和初始变换规则库
3. AI 运行 L2 搜索，生成候选列表 + 自动 L3 报告
4. 你做 L3 审查（10–30 分钟）：处理 UNKNOWN 升级，确认 SAFE/UNSAFE
5. AI 根据你的 L3 判断更新搜索策略 → 循环

你的时间只花在 L3 和方向决策上，其他都是 AI 的工作。

---

## 八、这样做值不值得

详见 `docs/assessment.md`。

简答：值得，前提是当作长期项目而非截止日期任务。

---

## 九、之后的方向（Phase 3 之后）

Phase 1 和 Phase 2 完成后，Illusion 将成为一个可以自动发现并验证判别性质的系统。之后的工作方向：

### Phase 4：MCP 接入 + 代数电路 — ✅ 完成

**4a** ✅ MCP server 骨架 + tool schema（`mcp/server.py`）
**4b** ✅ 文献检索辅助 L3（`mcp/l3_integration.py`，prompt 模式验证通过）
**4c** ✅ 自动变换生成骨架（`mcp/l2_integration.py`，含 `ExhaustionCriterion` 终止条件）
**4d** ✅ 代数电路领域验证，n=3，GF(7)（2026-05-09）
**4e** ✅ n=4 扩展验证，信号随 n 增强确认（2026-05-09）

**Phase 4 核心发现**：
1. L2 找到 `algebraic_restriction_p0.3/0.5`，Δcollapse ≈ +0.10–0.12 → SAFE（Razborov-Smolensky 类比）
2. `field_reduction_q2` Δ=+0.105，与 `algebraic_restriction_p0.3` 持平，但 L3 判 UNSAFE（局部操作）
3. n=4 验证：`algebraic_restriction` 信号增强（+0.104→+0.124），`field_reduction` 信号减弱（+0.105→+0.082）
4. MCP live 模式验证通过：客户端直接调用 LLM，绕过 subprocess 网络限制
5. 假阳性模式在单调域（`edge_deletion_p0.1`）和代数域（`field_reduction`）独立出现——L3 必要性的双重证据

详见 `docs/phase4d-report.md`。

---

### Phase 5：证明复杂度（Resolution）— ✅ 完成

**目标**：进入答案不完全已知的领域，让 L3 上报 UNKNOWN。

**结果（2026-05-09）**：

| 变换 | Δcollapse | L3 判定 |
|------|-----------|---------|
| clause_restriction_p0.2 | +0.600 | SAFE |
| clause_restriction_p0.4 | +0.780 | SAFE |
| clause_projection_p0.7 | +0.780 | SAFE |
| clause_projection_p0.8 | +0.780 | SAFE |
| variable_elimination_p0.2 | +0.640 | **UNKNOWN** |
| variable_elimination_p0.3 | +0.780 | **UNKNOWN** |

**核心发现**：
1. `clause_restriction` → SAFE：Ben-Sasson-Wigderson 宽度方法的 Resolution 类比，L2 在不知道该证明的情况下找到了它
2. `variable_elimination` → **UNKNOWN**（Δ=+0.64–0.78）：对应 Extended Resolution，Resolution 与 Extended Resolution 的分离是开放问题，L3 无法判定
3. 这是 Illusion 系统第一次上报 UNKNOWN——从验证工具到探索工具的转折点

详见 `docs/phase5-design.md`，论文草稿：`papers/illusion-proof-complexity.md`。

---

### Phase 5b：Frege 证明复杂度（深度度量）— ✅ 完成

**目标**：将框架扩展到 Frege 证明系统，以证明深度为资源界。

**结果（2026-05-10）**：

| 变换 | Δcollapse | L3 判定 |
|------|-----------|---------|
| variable_restriction_p0.2 | +0.600 | SAFE |
| variable_restriction_p0.3 | +0.200 | SAFE |
| hypothesis_projection_p0.7 | +0.600 | SAFE |
| hypothesis_projection_p0.8 | +0.600 | SAFE |
| hypothesis_weakening_e1 | +0.600 | SAFE |
| subformula_elimination_n2 | +0.000 | (rejected) |

**核心发现**：
1. `variable_restriction` / `hypothesis_projection` → SAFE：Krajíček 1994 的 Frege 下界技术类比
2. `subformula_elimination`（Extended Frege 输入级操作）信号为零——Extended Frege 的优势不在深度
3. UNKNOWN = 0 本身是信息：bounded-depth Frege 的下界已知（Krajíček-Pudlák 1995），没有开放问题需要上报
4. 这为 Phase 5c 提供了对照：同一架构，同一目标（PHP），不同度量

详见 `phase5b/results/` 实验报告。

---

### Phase 5c：Frege 证明复杂度（大小度量）— ✅ 完成

**目标**：以证明大小（总推导步数）为资源界，探测 Frege vs Extended Frege 分离。

**关键设计**：
- `enable_caching`：跨分支缓存（一个分支推导的 unit 在兄弟分支免费使用）= Extended Frege 的缩写机制
- `cross_branch_caching` 变换：不修改假设，只启用证明器的缓存模式
- 度量：step_limit=100 下 PHP(6,5) 标准 Frege 不可证，Extended Frege 可证

**结果（2026-05-10）**：

| 变换 | Δcollapse | L3 判定 |
|------|-----------|---------|
| variable_restriction_p0.2 | +1.000 | SAFE |
| variable_restriction_p0.3 | +0.625 | SAFE |
| hypothesis_projection_p0.7 | +1.000 | SAFE |
| hypothesis_projection_p0.8 | +1.000 | SAFE |
| cross_branch_caching_f1.0 | +1.000 | **UNKNOWN** |
| hypothesis_weakening_e1 | +1.000 | SAFE |
| hypothesis_weakening_e2 | +1.000 | SAFE |
| subformula_elimination_n2/n3 | +0.000 | (rejected) |

**核心发现**：
1. `cross_branch_caching` → **UNKNOWN**（Δ=+1.000，最大信号）：对应 Extended Frege 的缩写机制。Frege 与 Extended Frege 的 p-simulation 是证明复杂度的核心开放问题（Cook & Reckhow 1979）
2. Phase 5b（深度）vs 5c（大小）对照：同一操作在深度度量下信号为零，在大小度量下信号最大——框架精确定位了开放问题所在的度量维度
3. `subformula_elimination`（输入级缩写）信号为零——真正的 Extended Frege 优势在证明器内部的跨分支共享，不在输入变换
4. 跨阶段一致性：Phase 5（Resolution）发现 `variable_elimination` → UNKNOWN，Phase 5c（Frege）发现 `cross_branch_caching` → UNKNOWN。框架在每个域独立发现证明系统与其扩展之间的边界

**跨阶段对照表**：

| Phase | 域 | UNKNOWN 变换 | 对应开放问题 |
|-------|-----|-------------|-------------|
| 5 | Resolution | variable_elimination | Resolution vs Extended Resolution |
| 5b | Frege (depth) | (none) | — |
| **5c** | **Frege (size)** | **cross_branch_caching** | **Frege vs Extended Frege** |

详见 `phase5c/results/` 实验报告。

---

### Phase 5c 补充：Scaling Law — ✅ 完成

**目标**：量化 Frege vs Extended Frege 的分离规模随 PHP 大小的增长。

**结果（2026-05-10）**：

| PHP | Standard Frege | Extended Frege | 比率 |
|-----|---------------|---------------|------|
| PHP(3,2) | 8 步 | 7 步 | 1.1x |
| PHP(4,3) | 67 步 | 13 步 | 5.2x |
| PHP(5,4) | 525 步 | 21 步 | 25.0x |
| PHP(6,5) | >3000 步 | 30 步 | >100x |

**核心发现**：
- Extended Frege 步数多项式增长（O(n²)）
- Standard Frege 步数指数增长（约 8^n）
- 比率超多项式增长——与分离猜想一致
- 框架不只是指向开放问题，它量化了分离的规模

详见 `phase5c/results/scaling_report.md`。

---

### Phase 6（规划中）：千禧年难题 — RH

**目标**：将 Illusion 的闭包搜索范式应用于黎曼猜想。

**方法**：不是试图证明 RH，而是：
1. 用 α 诊断为什么当前方法失败
2. 用闭包四定律（对偶、刚性、显性对称、高维到低维）约束候选证明路径
3. 在约束空间里搜索满足四定律的候选闭包

**已有基础**：
- `docs/symbol-system.md` §4.5：RH 的符号标注
- `docs/symbol-system.md` §6：闭包四定律定义 + RH 实例（Hilbert-Polya）
- Manifesto "A Diagnosis" 节：结构分析

**待实现**：
- L1：解析数论模型（ζ 函数零点、显式公式）
- L2：闭包搜索（在算子空间中搜索满足四定律的 H_RH）
- L3：验证候选闭包是否真的在 M_an 之外

### 符号体系

详见 `docs/symbol-system.md`。

核心定位：不是独立的公理系统，是对已有数学证明的结构标注工具。每个关系符号带模型下标 M，标注推导步骤在 M 内还是 M 外。与论文 §2 定义和 §6.7.3 SRS 指数严格对应。

**当前状态（2026-05-07）**：工作文档完成。包含核心符号表、SRS 数值化、4 个标注实例（AC⁰、Monotone、Gödel、NS）、已知误用模式、开放问题。等 MCP 4b 完成后，第一个需要符号参与判定的场景会出现。

### NS 千禧年问题方向（探索性）

来源：2026-05-07 与 Deepseek 的符号探索。

核心发现：用 SRS 框架分析 3D NS 千禧年问题，得到 α ≳ 10¹⁰（Re=10⁴），且 α 随 Re → ∞ 发散。2D NS 的 α ≈ 1（涡度最大值原理将判定成本压至 poly）。这支持"NS 全局光滑性在当前最佳解析模型内不可判定"的猜想。

**状态**：结构化猜想，不是证明。需要数值实验支撑。候选降阶工具：低维动力系统（涡管曲率/间距/核心半径的封闭演化方程）。详见 `inspiration/response/2026-5-7-Deepseek-Rewrite-NS-equation.md`。

**优先级**：低于 MCP 4b-4d 和代数电路。但如果 Illusion 的 L2 搜索能力增强后，可以用来搜索涡管动力系统的候选判别量。

### 从 AC⁰ 到更强模型

Phase 1（AC⁰）、Phase 3（单调电路）、Phase 4d/4e（代数电路）已完成。信号随 n 增强在 Phase 3（n=6→8 待验证）和 Phase 4e（n=3→4 已验证）均有支持。之后扩展路径：
- 证明复杂度（L1 = Resolution/Frege）← **Phase 5 当前目标**
- 形式系统（L1 = PA/ZFC 的可证明性）← 远期

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
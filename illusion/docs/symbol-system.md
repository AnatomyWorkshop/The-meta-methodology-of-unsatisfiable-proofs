# 符号体系：自指安全标注语言

> 日期：2026-05-07
> 状态：工作文档。随实验迭代更新。
> 来源：论文 §2 定义 + §6.7.3 SRS 指数 + 与 Deepseek/Doubao 的符号探索（2026-05-06/07）
> 定位：Illusion 框架的符号层。不是独立的公理系统，是对已有数学证明的结构标注工具。

---

## 0. 设计原则

1. **模型下标是心脏。** 每个关系符号都带下标 M，锚定在具体的计算模型上。没有 M，符号没有语义。
2. **不是替代数学，是增强。** 这套符号在传统证明之上加一层结构标注：哪些步骤在 M 内，哪些在 M 外，哪些等价关系在 M 内不可判定。
3. **不是公理系统，是翻译工具。** 当 M 固定后，这些符号可以把传统证明翻译成带安全性标注的证明图谱。它们不产生新证明，只标注已有推导的安全等级。
4. **符号克制。** 只引入有操作性语义的符号。每个符号都必须回答"什么条件下使用它"和"谁来判定这个条件"。

---

## 1. 核心符号表

### 1.1 推导关系（箭头族）

| 符号 | 读法 | 语义 | 判定者 |
|------|------|------|--------|
| $\to_M$ | "M 内可推导" | 从前提到结论的推导链，每一步都在 M 的能力范围内 | L2（自动验证） |
| $\nrightarrow_M$ | "M 内不可达" | M 内的操作无法从前提到达结论 | L3（安全检查） |
| $\Rrightarrow_M$ | "M 外操作" | 使用了超出 M 能力的外部工具 | L3（标注来源） |

**使用规则：**
- $A \to_M B$：M 内存在从 A 到 B 的推导链。推导链的每一步都是 M 内可判定的操作。
- $A \nrightarrow_M B$：不存在这样的推导链。这是 L3 的核心判定——如果 L3 判定某个性质 P 满足 $P \nrightarrow_M \text{decidable}$，则 P 是自指安全的。
- $A \Rrightarrow_M B$：从 A 到 B 的推导使用了 M 外的工具。这些工具在 M 内不可模拟。

**注意：** $\to_M$ 不区分单步和多步。如果将来需要区分推导粒度，再引入新符号。当前不需要。

### 1.2 等价关系

| 符号 | 读法 | 语义 | 安全等级 |
|------|------|------|----------|
| $\equiv_M$ | "M 内结构等价" | 两个对象在 M 的结构度量下不可区分 | SAFE |
| $\simeq_M$ | "M 内外延等价" | 两个对象在 M 的输出上相同，但结构不同 | 需要 L3 检查 |
| $\approx_M$ | "M 内不可判定等价" | M 内无法判定两者是否等价 | 只能作为公理假设 |

**操作性语义：**
- $X \equiv_M Y$：M 内存在一个可判定的过程，验证 X 和 Y 在结构上相同。例如：两个 AC⁰ 电路的门结构同构（可在 poly(n) 时间内验证）。
- $X \simeq_M Y$：X 和 Y 在某种外延度量上等价，但 M 内无法验证结构相同。例如：两个变换对同一组测试电路产生相同的 collapse 值，但它们的操作方式不同（random restriction vs exhaustive parity check）。
- $X \approx_M Y$：M 内无法判定两者是否等价（需要超出 M 的资源）。例如：判定"random restriction 后的电路"和"某个已知常数函数"是否在所有输入上等价，需要穷举 2ⁿ 个输入。

**谁来判定归类？** L3。当 L2 生成一个候选等价关系时，L3 检查：这个等价性的验证过程是否在 M 内可完成？如果是，标 $\equiv_M$；如果只有外延可验证，标 $\simeq_M$；如果连外延都不可验证，标 $\approx_M$。

### 1.3 能力关系

| 符号 | 读法 | 语义 |
|------|------|------|
| $\sqsubset_M$ | "M 内严格弱于" | 在 M 的度量下，A 的能力是 B 的真子集 |
| $\mathring{\sqsubset}_M$ | "M 内公理级分离" | A 和 B 的分离在 M 内不可判定，但可作为外部假设引入 |

**$\mathring{\sqsubset}_M$ 的精确定义：**

$$A \mathring{\sqsubset}_M B \quad\iff\quad (A \nrightarrow_M B) \;\land\; (B \nrightarrow_M A) \;\land\; \text{Con}(M + A \sqsubset B)$$

读作：在 M 内，A 和 B 的分离既不可证也不可驳，但假设 A 严格弱于 B 不会破坏 M 的一致性。

**典型实例：**
- $P \mathring{\sqsubset}_{P/poly} NP$：在多项式电路模型内，P 和 NP 的分离不可判定，但假设 P≠NP 不破坏一致性。
- $\text{Con}(F) \mathring{\sqsubset}_F \text{True}$：在形式系统 F 内，F 的一致性不可证，但假设 F 一致不破坏 F。

### 1.4 量词

| 符号 | 读法 | 语义 |
|------|------|------|
| $\forall_M$ | "M 内任意" | 对 M 内所有可枚举的对象 |
| $\exists_M$ | "M 内可构造" | M 内存在一个可构造的对象 |

**注意：** 当 M 的对象空间不可枚举时（如实数），$\forall_M$ 退化为标准全称量词。下标 M 在这种情况下只标注"这个量化发生在 M 的语境中"，不额外约束枚举性。

### 1.5 模型扩展

当需要表示"引入外部工具后的新模型"时：

$$M^* = M \cup \{T^*\}$$

其中 $T^*$ 是一个不在 M 内的新工具。扩展模型 $M^*$ 的 SRS 可能低于 M 的 SRS：

$$\alpha_{M^*}(P) \leq \alpha_M(P)$$

如果 $T^*$ 能把 α 从 ≫1 压到 ≈1，则 P 在 $M^*$ 内可判定。这是"降阶"的精确含义。

### 1.6 粒度关系（非标准实数扩展，2026-05-10）

当需要刻画"差一个无穷小"的精细结构时，引入基于非标准实数 ${}^*\mathbb{R}$ 的三个粒度符号：

| 符号 | 读法 | 定义 | SRS 语义 |
|------|------|------|----------|
| $a \prec b$ | "无穷小弱于" | $0 < b-a$ 是无穷小 | 差异在 M 内不可分辨，被坍缩为 0 |
| $a \approx_\epsilon b$ | "超逼近等价" | $b - a$ 是无穷小 | 标准视角相等，非标准视角存在结构间隙 |
| $a \ll b$ | "严格强小于" | $\text{st}(b-a) > 0$ | 差异宏观可辨，在 M 内可判定 |

**与现有符号的对应：**

| 粒度符号 | 对应的 SRS 状态 | 对应的等价关系 |
|----------|----------------|---------------|
| $\ll$ | $\alpha \gg 1$（宏观分离） | — |
| $\prec$ | $\alpha \gtrsim 1$（UNKNOWN 边界） | $\simeq_M$（外延等价，结构不等价） |
| $\approx_\epsilon$ | $\alpha = 1 + \epsilon$（门槛处） | $\simeq_M$ 到 $\equiv_M$ 的过渡 |

**典型实例：**
- Connes 迹公式与黎曼显式公式：$\text{Connes} \approx_\epsilon \text{RH 显式公式}$（数值完全匹配，结构间隙 = 算子良定义性）
- 模型分辨极限：$\epsilon$ 定义了模型 M 的最小可分辨粒度，小于此粒度的差异在 M 内被强制坍缩为相等

**设计决策：** 这套符号是 SRS 的可选扩展层。核心判定仍然是 $\nrightarrow_M$（定性）和 α（定量）。粒度符号在需要描述"接近但未跨过门槛"的状态时使用。

---

### 2.1 定义

$$\text{SRS}(M, P) = \frac{\text{判定 P 所需的最小计算资源}}{\text{M 内可用的最大计算资源}}$$

| α 值 | 含义 | 安全等级 |
|------|------|----------|
| α ≤ 1 | P 在 M 内可判定 | UNSAFE（自指不安全） |
| α > 1 | P 在 M 内不可判定 | SAFE（自指安全） |
| α = ∞ | P 在 M 内不可达（哥德尔级） | SAFE（结构性不可判定） |

### 2.2 已验证的数值

| 案例 | n | α（数值） | 标度律 |
|------|---|----------|--------|
| AC⁰ vs PARITY | 8 | ≈ 10² | 3ⁿ / poly(n) |
| Monotone vs CLIQUE | 6 | ≈ 9.1×10² | 2^{n(n-1)/2} / poly(n) |
| Gödel | — | ∞ | — |
| 2D NS（对照） | — | ≈ 1 | poly(Re) / poly(Re) |
| 3D NS（估计） | Re=10⁴ | ≳ 10¹⁰ | Re³ / O(1) → ∞ |

### 2.3 代数对应物（方向性）

论文 §6.7.3 提出的张量秩比版本：

$$\text{SRS}_\otimes(M,P) = \frac{\text{rank}(X_P)}{\max_{A \in M} \text{rank}(X_A)}$$

其中 $X_P$ 是区分性质 P 诱导的代数对象，$X_A$ 是模型内候选者诱导的代数对象。当 $\text{SRS}_\otimes > 1$，区分性质的代数复杂度超出模型内任何对象的代数复杂度。这个定义在代数电路领域（Phase 4d）会变成实际需求。当前标注为"研究方向"，不是精确定义。

### 2.4 紧凑记法

当需要在行内标注一个性质的安全等级时：

$$\alpha_M(P) \approx 10^2 \gg 1 \quad \Rightarrow \quad P \text{ 对 M 自指安全}$$

或在证明标注中直接写：

$$P \nrightarrow_M \text{可判定} \quad (\alpha \approx 10^2)$$

括号内的 α 值是辅助信息，不是符号体系的核心。核心判定仍然是 $\nrightarrow_M$（定性）；α 提供定量支撑。

---

## 3. 证明标注的工作流

给定一个传统证明，用这套符号标注的步骤：

1. **定模型 M**：明确被分析的计算模型或形式系统。
2. **标注每一步**：每个推导步骤标 $\to_M$（M 内）或 $\Rrightarrow_M$（M 外）。
3. **标注等价关系**：每个等价性断言标 $\equiv_M$、$\simeq_M$ 或 $\approx_M$。
4. **识别区分性质 P**：找到证明中那个"M 内不可判定"的核心性质。
5. **计算 SRS**：估算 α = cost(P) / cap(M)。
6. **安全判定**：α > 1 → SAFE；α ≤ 1 → UNSAFE。

---

## 4. 已完成的标注实例

### 4.1 AC⁰ vs PARITY（Phase 1）

$$M = AC^0 \text{ (深度 } d \text{, 规模 poly(n), AND/OR/NOT)}$$
$$f = \text{PARITY}$$
$$P = \text{"random restriction 后电路坍塌为常数"}$$

$$P \nrightarrow_{AC^0} \text{可判定} \quad (\alpha \approx 10^2)$$
$$\text{random\_restriction} \Rrightarrow_{AC^0} \text{坍塌}$$
$$\therefore P \text{ 是自指安全的判别性质}$$

### 4.2 Monotone vs CLIQUE（Phase 3）

$$M = \text{单调电路 (AND/OR only, poly(n))}$$
$$f = k\text{-CLIQUE}$$
$$P = \text{"subgraph projection 后电路无法区分 } D^+ \text{ 和 } D^-\text{"}$$

$$P \nrightarrow_{\text{Monotone}} \text{可判定} \quad (\alpha \approx 9.1 \times 10^2)$$
$$\text{subgraph\_projection} \Rrightarrow_{\text{Monotone}} \text{区分能力丧失}$$
$$\therefore P \text{ 是自指安全的判别性质}$$

### 4.3 哥德尔不完备定理

$$M = F \text{ (一致且充分表达的形式系统)}$$
$$G_F \equiv_M \neg\text{Prov}_M(G_F) \quad \text{(对角引理，M 内构造)}$$
$$G_F \nrightarrow_M \text{可证} \quad (\alpha = \infty)$$
$$\mathbb{N} \models G_F \quad (\Rrightarrow_{\mathbb{N}} \text{真，标准模型元语言})$$

### 4.4 NS 千禧年问题（探索性）

$$M_{\text{NS}} = \text{3D 不可压缩 NS + 当前最佳解析工具}$$
$$P_{\text{smooth}} = \forall \boldsymbol{u}_0 \in C^\infty: \text{全局光滑解存在}$$

$$P_{\text{smooth}} \nrightarrow_{M_{\text{NS}}} \text{可证} \quad (\alpha \gtrsim 10^{10}, \text{Re}=10^4, \text{conjectured})$$
$$\neg P_{\text{smooth}} \nrightarrow_{M_{\text{NS}}} \text{可证} \quad \text{(conjectured)}$$
$$\therefore P_{\text{smooth}} \mathring{\sqsubset}_{M_{\text{NS}}} \text{True?} \quad \text{(候选公理级分离)}$$

### 4.5 黎曼猜想（探索性，2026-05-10）

$$M_{\text{an}} = \{\text{解析数论},\ \zeta(s),\ L\text{-函数},\ \text{复分析}\}$$
$$M^* = M_{\text{op}} \cup M_{\text{adele}} = \{\text{自伴算子},\ \text{谱理论}\} \cup \{\text{阿黛尔},\ p\text{-进}\}$$
$$P_{\text{RH}}: \zeta(\rho) = 0,\ \rho \text{ 非平凡} \implies \Re(\rho) = \tfrac{1}{2}$$

$$P_{\text{RH}} \mathring{\sqsubset}_{M_{\text{an}}} \quad (\alpha \gg 1)$$
$$Q_{\text{HP}} = \exists H_{\text{RH}} \text{ 自伴},\ \text{Spec}(H_{\text{RH}}) = \{\gamma \mid \zeta(\tfrac{1}{2}+i\gamma)=0\}$$
$$Q_{\text{HP}} \nrightarrow_{M_{\text{an}}} \text{可判定} \quad \text{（闭包在原模型外）}$$
$$Q_{\text{HP}} \to_{M^*} P_{\text{RH}} \quad \text{（自伴性 ⇒ 谱全实 ⇒ RH）}$$
$$\alpha(M^*, Q_{\text{HP}}) \sim 1$$

当前状态：$\text{Connes 迹公式} \simeq_{M_{\text{an}}} \text{黎曼显式公式}$（外延匹配，结构间隙未闭合）。

Illusion 的构造目标：在候选算子空间中搜索满足闭包四定律的 $H_{\text{RH}}$。

---

## 5. 已知的误用模式

在符号探索过程中（2026-05-06/07），以下误用被识别并修正：

1. **把定义写成公理。** 实数的加法交换律不是公理——它是实数域的定义性条件。AC⁰ ⊏ NC¹ 不是公理——它是已证明的定理。单调电路不含非门不是公理——它是模型的定义。只有那些"可以假设也可以不假设，且假设后不破坏一致性"的命题，才能用 $\mathring{\sqsubset}_M$ 标注为公理级分离。

2. **混淆"外部推理"和"选择"。** $\Rrightarrow_M$ 是"外部工具推出了一个结论"，不是"人类选择了一个假设"。"P≠NP 是最优公理"不能写成 $\Rrightarrow_M$，因为这是一个元层次的选择，不是一个推理步骤。正确写法是 $\mathring{\sqsubset}_M$。

3. **对不同证明用同一个 $\Rrightarrow_M$ 而不区分外部工具的性质。** 停机问题的"外部"是纯逻辑对角化（M 自己干掉了自己）；哥德尔句的"外部"是标准模型的语义解释；CLIQUE 下界的"外部"是组合构造。它们的 $\Rrightarrow_M$ 语义不同。当前符号体系不区分这些子类——这是有意的简化。如果将来需要区分，可以引入 $\Rrightarrow_M^{\text{diag}}$、$\Rrightarrow_M^{\text{sem}}$、$\Rrightarrow_M^{\text{comb}}$ 等上标。暂不引入。

---

## 6. 闭包四定律（闭包搜索范式，2026-05-10）

当 L2 的搜索目标从"判别性质"扩展到"闭包"时（即从证明下界扩展到证明千禧年命题），候选闭包 $Q$ 必须同时满足以下四条结构约束：

### 6.1 定义

设 $P_{\text{target}}$ 为目标命题，$M_{\text{int}}$ 为当前主流工具构成的内模型，$M^*$ 为扩展模型。

**合法闭包** $Q_{\text{closure}}$ 满足：
- $Q \nrightarrow_{M_{\text{int}}}$ 可判定（Q 必须源于外部）
- $Q \to_{M^*}$ 可判定（Q 在扩展模型中有明确真值）
- $Q \land \neg P_{\text{target}} \to \bot$（Q 与命题否定矛盾）

### 6.2 四定律

在无数合法 $Q$ 中，只有同时满足以下四条的才是通往证明的有效路径：

| 定律 | 内容 | 操作性检验 |
|------|------|-----------|
| **对偶性** | $Q$ 在两个原本无关的数学领域间建立精确对偶 | 存在双射或函子连接两个域 |
| **刚性** | $Q$ 导出一个没有自由度的刚性结构 | 结论是二元的（有/无），不允许连续扰动 |
| **显性对称** | $Q$ 将问题的隐蔽对称性显性化为刚性结构的自然属性 | 原问题的对称群在 $Q$ 中有显式表示 |
| **高维到低维** | $Q$ 将原命题的无穷复杂性压缩到有限维或离散的不变量上 | 存在降维映射，且映射保持关键信息 |

### 6.3 已知实例

| 目标 | 闭包 $Q$ | 对偶 | 刚性 | 显性对称 | 高维→低维 |
|------|----------|------|------|----------|-----------|
| $P_{\text{RH}}$ | 希尔伯特-波利亚 $H_{\text{RH}}$ | 零点↔谱 | 自伴性 | 函数方程↔$\Theta$ | 素数分布→单一算子 |
| $P_{\text{smooth}}$ (NS) | 低维动力系统闭包 | 全流场↔$(\kappa,\delta,\sigma)$ | 有限时间爆破是二元的 | NS 标度不变性↔动力系统对称 | 3D PDE→3D ODE |

### 6.4 与 Illusion 架构的关系

- **L1** = $M_{\text{int}}$（被分析的内模型）
- **L2** = 在扩展模型空间中搜索满足四定律的 $Q_{\text{closure}}$
- **L3** = 验证候选闭包是否真的在 $M_{\text{int}}$ 之外（$\alpha > 1$）

Phase 1–5 中，L2 搜索的是判别性质（证明下界的工具）。远期目标中，L2 搜索的是闭包（证明千禧年命题的工具）。架构不变，搜索空间的维度变了。

---

## 7. 内涵外延张力的处理

论文 §6.4 承认：同一个"自指安全"定义，操作在外延对象（电路族）和内涵对象（形式系统）上。

这套符号的处理方式：**把差异封装进 M 的定义里，符号层保持统一。**

- 当 M 是外延的（电路模型）：$\in_M$ 是语法检查（深度、规模、门类型）
- 当 M 是内涵的（形式系统）：$\in_M$ 是一致性 + 表达能力检查

$\nrightarrow_M$ 在两种情况下语义相同："M 内的操作到不了 P"。操作的具体含义由 M 的性质决定，符号本身不暴露这个差异。

如果将来需要显式区分：
$$M_{\text{ext}} \quad \text{vs} \quad M_{\text{int}}$$

但当前不需要。张力被 M 的定义吸收了。

---

## 8. 与论文定义的对应

| 论文定义 | 符号对应 |
|----------|----------|
| Definition 2.3 (Discriminating property) | P 满足 Necessity + Conflict |
| Definition 2.4 (Self-referential safety) | $P \nrightarrow_M \text{decidable}$, 即 α > 1 |
| First Law (Safety Condition) | 有效的不可能性证明必须使用 α > 1 的 P |
| Second Law (Generalization Barrier) | 从 M₁ 到 M₂ 时，P 的 α 可能从 >1 变为 ≤1 |
| Third Law (Meta-Methodological Constraint) | 诊断 α 的框架本身不在 M 内 |
| §6.7.3 SRS Index | α = cost(P) / cap(M) |

---

## 9. 这套符号不做什么

- **不是独立的公理系统。** 它不产生新定理。它标注已有定理的结构。
- **不替代传统数学。** 传统证明仍然是证明。这套符号是在证明之上加的一层元数据。
- **不自动化 L3。** 符号标注本身需要 L3 判定（"这个等价性在 M 内可判定吗？"）。符号不能替代判定，只能记录判定结果。
- **不处理自身的自指安全。** L3 的标注只给 L2 用，不给自己用。这是设计约束，不是缺陷。（参见 `note-equivalence-annotation.md` 的"自噬问题"讨论。）

---

## 10. 开放问题

1. **$\to_M$ 的粒度**：当前不区分单步和多步。如果 MCP 接入 Lean 后需要标注证明树的每一步，可能需要引入 $\to_M^{(1)}$（单步）和 $\to_M^{(*)}$（多步闭包）。
2. **PDE 演化的标注**：NS 案例中，"解随时间演化"不是推导，是动力学过程。候选符号：$\leadsto_M$（M 内演化，终点未知）。暂不引入。
3. **代数对应物**：论文 §6.7.3 提出 $\text{SRS}_\otimes(M,P) = \text{rank}(X_P) / \max_{A \in M} \text{rank}(X_A)$。这个方向在代数电路领域（Phase 4d）会变成实际需求。
4. **等价性标注的操作性语义**：什么条件下一个等价性被归类为 $\simeq_M$ 而不是 $\equiv_M$？第一个具名实例已出现：Connes 迹公式与黎曼显式公式的关系是 $\simeq_{M_{\text{an}}}$（数值匹配，结构间隙）。
5. **$\Rrightarrow_M$ 的粒度**：不同证明的外部操作性质不同（对角化、语义解释、组合构造）。候选上标：$\Rrightarrow_M^{\text{diag}}$、$\Rrightarrow_M^{\text{sem}}$、$\Rrightarrow_M^{\text{comb}}$。Lean/Coq 接入时可能需要。
6. **闭包四定律的形式化**：当前四定律（对偶、刚性、显性对称、高维到低维）是结构性描述。是否可以给出操作性判定标准？需要更多实例（P vs NP、BSD）来检验。
7. **粒度符号的边界**：$\prec$ 和 $\approx_\epsilon$ 在什么条件下比 $\simeq_M$ 提供更多信息？需要在 PDE 和数论领域积累具体案例。

---

## 11. 触发条件

以下情况出现时，更新本文档：
1. MCP 接入后，L2 生成的候选变换需要用这些符号描述
2. 代数电路领域（Phase 4d）需要 $\text{SRS}_\otimes$ 的具体定义
3. MCP 接入 Lean/Coq 后，等价性标注的操作性语义需要被形式化
4. 论文修订时，需要把这些符号写进正式定义
5. Illusion 应用于千禧年难题时，闭包四定律需要被检验和修正
6. 粒度符号在具体案例中被使用后，评估是否纳入正式论文

---

*这份文档是工作文档，不是最终设计。符号体系会随实验迭代而演化。当前版本的目标是：让一个没参与对话的人，读完后能用这些符号标注一个已知的不可能性证明——或者用闭包四定律评估一个候选证明路径。*

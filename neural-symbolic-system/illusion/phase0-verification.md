# Phase 0 验证报告：框架的反向验证与压力测试

> 目标：在动手实现原型之前，验证框架（Definition 6.4）的归纳基础是否稳固
> 状态：核心验证完成，发现两个边界案例需要回应

---

## 一、核心验证：Razborov-Smolensky AC⁰[p] 下界

### 来源
- Smolensky (1987) STOC 原文
- Goldreich 教学长文（一般情形 p≠q）
- MIT 课程笔记（p=3 特例）
- Razborov (1995) 元理论限制论文

### 代入 Definition 6.4

| 组件 | 代入值 |
|------|--------|
| 模型 M | AC⁰[p] 电路族（常数深度 d，多项式大小，AND/OR/NOT/MOD_p 门） |
| 目标 f | 计算 MOD_q（q≠p，均为素数），理想值 v* = 0 误差 |
| 判别性质 P | "可被 GF(p) 上低次（≤√n）多项式逼近" + "MOD_q 具有 U_F-完全性" |
| P 在 M 内可判定？ | **否** — 需要模 q 计数与指数级多项式搜索，M 只能做模 p 计数 |
| 自指安全性 | **安全 ✅** |

### 证明结构

1. P₁（逼近性）：AC⁰[p] 电路的计算可被 GF(p) 上低次多项式以极高概率逼近
2. P₂（不可逼近性）：MOD_q 不能被任何 GF(p) 上低次多项式有效逼近
3. 矛盾：若 C 完美计算 MOD_q，则由 P₁ 得低次逼近，与 P₂ 矛盾

### 为什么 P 在 AC⁰[p] 内不可判定

判定"是否存在逼近 MOD_q 的低次多项式"需要：
- 在 GF(p) 的扩域中使用 q 次本原单位根 ω
- 搜索指数级大小的多项式空间
- 模拟模 q 计数（因为 ω 的指数追踪了模 q 的和）

AC⁰[p] 的核心数值能力限于模 p 的和。由于 p≠q 且均为素数，AC⁰[p] 甚至不能计算模 q。

### 额外收获：razborov95.pdf 的元理论呼应

Razborov (1995) 证明了：如果存在足够强的伪随机生成器，则某些有界算术系统不能反驳"小电路计算 SAT"。这从元理论角度印证了第三定律——证明下界的元方法本身也不能落在被分析模型的内部。

**结论：Razborov-Smolensky 完全符合 Definition 6.4。框架的归纳基础得到加强。**

---

## 二、压力测试：六类额外案例

### 测试 1（高威胁）：Williams ACC⁰ 下界 (2014) — 范式外证明

- **证明方法**：算法方法（去随机化 + 矩阵乘法加速 SAT），不使用判别性质范式
- **模型 M**：ACC⁰（带任意模计数门的常数深度电路）
- **判别性质 P**：**找不到传统的 P**。证明逻辑是"如果 M 能计算 f，则可用 M 加速一个 M 之外的算法，导致矛盾"
- **对框架的威胁**：Theorem 6.5 说"如果存在自指安全的 P，则构成不可满足性证书"。Williams 证明了不存在显式 P 也能证明下界。
- **诊断**：这不是框架的错误，而是框架的**边界**。框架刻画的是"基于判别性质的下界证明"的结构前提，不排斥算法式下界等非构造性方法。
- **需要的修正**：在 §6.2 或 §6.7 补充适用范围声明（Scope Clause）

### 测试 2（安全，强化）：Gupta-Kamath-Kayal-Saptharishi 永久多项式深度-3 下界 (2013)

- **模型 M**：多项式大小的 ΣΠΣ 电路（深度 3，特征 0 或大域）
- **目标 f**：永久多项式 Perm_n
- **判别性质 P**：偏导数矩阵的秩 / Shifted-Partial-Derivatives 测度超过阈值
- **自指安全检查**：计算多项式的偏导数矩阵秩通常需要 #P-hard 或指数时间。深度-3 电路无法计算这个全局代数不变量。
- **结论**：**安全 ✅**。验证了框架的跨域泛化能力（布尔 → 代数电路）。可补充进 §6.5.3。

### 测试 3（安全，强化）：Razborov 不相交性通信复杂度下界 (1992)

- **模型 M**：深度为 d 的通信协议
- **目标 f**：不相交性函数 DISJ_n
- **判别性质 P**：在某个单射随机分割下，矩阵的秩超过阈值
- **自指安全检查**：浅层通信协议不能计算矩阵的秩（需要多项式对数深度通信量）
- **结论**：**安全 ✅**。填补了 §6.7.7 提到的通信复杂度空白。

### 测试 4（极度危险）：PHP 扩展 Frege 尺寸-宽度下界 — 量词陷阱

- **模型 M**：扩展 Frege 证明系统
- **目标 f**：证明鸽巢原理 PHP
- **判别性质 P（初步）**："证明的最大公式宽度 < w"
- **陷阱**：判定"某个给定证明的宽度 < w"只需多项式时间（遍历每一行）。如果 P 在 M 内可判定，则根据 Definition 6.4 它是自指不安全的——但这是一个**成功的下界**！
- **化解**：真正的判别性质不是"这个证明宽度小"，而是"**存在**一个宽度小且步数少的证明"（Σ₂ 性质）。判定"是否存在"需要搜索指数级证明空间，超出扩展 Frege 自身能力。
- **需要的修正**：Definition 6.4 需要增加量词敏感性条款（Scope Clause），排除多项式时间可验证的局部语法性质，要求 P 是针对"所有/存在满足理想值的候选者"的全局性质。

---

## 三、对框架的修正建议

Phase 0 发现了两个需要回应的问题：

### 修正 1：适用范围声明

在 §6.2 的 Remark 或 §6.7 补充：

> "The framework characterizes the structure of *discriminating-property-based* lower-bound proofs. It does not claim to subsume all proof methods — in particular, algorithmic lower bounds (e.g., Williams 2014) that proceed by self-reduction rather than by identifying a discriminating property fall outside the framework's scope. This is a limitation of coverage, not a contradiction."

### 修正 2：量词敏感性条款

在 Definition 6.4 的 Remark 中补充：

> "The discriminating property P must be understood as a *global* predicate over the search space S — typically involving an existential or universal quantifier over candidates. A local syntactic check on a single candidate (e.g., 'this proof has width < w') may be decidable within M, but the corresponding global property ('there exists a proof of width < w and size < s') typically requires exponential search and is not decidable within M. The self-referential safety condition applies to the global form."

### 这两个修正的性质

这不是框架的失败。这是框架的**精确化**。Phase 0 的目的就是找到这些边界，在写代码之前把理论地基打稳。

---

## 四、Phase 0 结论

| 验证项 | 结果 | 对框架的影响 |
|--------|------|-------------|
| Razborov-Smolensky AC⁰[p] | 安全 ✅ | 归纳基础加强 |
| Gupta et al. 代数深度-3 | 安全 ✅ | 跨域泛化验证 |
| Razborov DISJ 通信复杂度 | 安全 ✅ | 填补 §6.7.7 空白 |
| Williams ACC⁰ (2014) | 框架不适用 ⚠️ | 需要适用范围声明 |
| PHP 扩展 Frege | 量词陷阱 ⚠️ | 需要量词敏感性条款 |

**总判断**：框架的核心（Definition 6.4 + 三定律）在所有基于判别性质的下界证明中成立。两个边界案例不是反例，而是框架适用范围的精确标定。理论地基稳固，可以进入 Phase 1。

---

## 五、下一步

1. **立即**：把修正 1 和修正 2 写进论文的 §6.2 和 §6.7
2. **本周**：如果要进一步加强归纳基础，可以显式检查 Williams 2014 是否真的没有隐式的判别性质（有些分析认为其"矩阵嵌入"步骤可以被重新解读为一种非标准的 P）
3. **Phase 1**：开始实现 AC⁰ 玩具系统

### 去哪里找更多案例

- **ECCC**（Electronic Colloquium on Computational Complexity）：最新的下界证明预印本
- **arXiv cs.CC**：计算复杂度分类
- **CCC 会议论文集**（Computational Complexity Conference）：每年最集中的下界证明
- **Ryan Williams, Lijie Chen, Igor Oliveira** 的近期工作：他们在 meta-complexity 方向最活跃
- **Forbes-Shpilka-Tzameret-Wigderson (2021)**：代数电路 → 证明复杂度的归约（已在 association 文档中诊断为安全）

# Code Review — Illusion Phase 1

> 日期：2026-05-03
> 审阅方式：先读代码，理解功能，再读论文，最后回顾代码

---

## 一、代码功能理解（读论文之前）

### 整体架构

Illusion 是一个三层搜索系统，用于在 AC⁰ 电路领域验证"自指安全判别性质"能否被机器自主发现：

```
L3（自反层）：l3_monitor.py → 规则库模式匹配，判断候选性质的 SAFE/UNSAFE/UNKNOWN
L2（判别层）：l2_search.py + transforms.py → 枚举变换，测量 collapse，筛选候选
L1（对象层）：l1_circuit.py → 随机 AC⁰ 电路生成 + PARITY 目标函数
评估辅助：evaluator.py → 蒙特卡洛错误率估计
实验编排：run_experiment.py → 串联全部流程
```

### 各模块功能

**l1_circuit.py**：AC⁰ 电路模拟器。门类型：AND/OR/NOT/INPUT，无界扇入。电路按拓扑序存储，逐层交替使用 AND/OR。`random_ac0_circuit` 生成随机电路（每层门数 = n/(depth+1)，扇入 2-6，30% 概率取反）。`parity` 函数是真值表中奇数个 True 返回 True。

**transforms.py**：8 个变换构成 L2 搜索空间：
- `RandomRestriction`（p=0.3/0.5/0.7）：Håstad Switching Lemma 的核心变换
- `InputPermutation`：控制变换（置换不变性）
- `GateSubstitution`（两种方向）：AND↔OR 替换
- `DepthReduction`：压缩底部两层
- `ExhaustiveParityEquivalentCheck`：压力测试变换（穷举等价性检查）

**l2_search.py**：核心逻辑——对每个变换，应用到 50 个随机 AC⁰ 电路，测量 collapse score（1 - 归一化方差）和 PARITY 是否受影响。候选条件：collapse > 0.15 且 PARITY 不受影响。

**l3_monitor.py**：规则库包含 UNSAFE 模式（permut/symmetr/invariant/monoton/linear/constant/depth_reduc/gate_substit/exhaustive_parity_equivalent）和 SAFE 模式（random_restrict/approximat/algebraic_degree）。正则匹配后输出 verdict + reason + reference。

**evaluator.py**：蒙特卡洛误差率估计，附带标准误差。

---

## 二、读论文之后的反向对照

论文的核心定义（Definition 2.4）：

> 判别性质 P 是自指安全的，当且仅当模型 M 中不存在任何候选对象能判定 P。

在 Illusion 中：
- M = AC⁰ 电路
- P = "该电路在变换 T 下坍塌"
- 如果 P 在 AC⁰ 内可判定 → UNSAFE（丢弃）
- 如果 P 需要指数枚举等超出 AC⁰ 的计算 → SAFE（保留）

代码正确地实现了这个区分。具体来说：

| 变换 | 为什么 SAFE/UNSAFE | 对应论文概念 |
|---|---|---|
| random_restriction | 判定坍塌需要枚举 exp(n) 个限制，超出 AC⁰ | 符合 Definition 2.4 |
| input_permutation | 判定置换不变性只需 n! 次检查，多项式时间 | 违反自指安全 |
| gate_substitution/depth_reduction | 判定电路结构性质在 AC⁰ 内可判定 | 违反自指安全（且被 L2 过滤） |
| exhaustive_parity_equivalent | 指数枚举但无结构性洞察 | 论文 Remark 的核心区分 |

**关键的匹配点**：

1. **collapse score 的设计**与论文的直觉一致：Håstad 的方法本质是让 AC⁰ 电路在随机限制下"坍塌"，collapse = 1 - Var/0.25 是一个聪明的代理度量。

2. **L3 规则库中的 "exponential ≠ safe" 区分**——`exhaustive_parity_equivalent_check` 被标记为 UNSAFE，理由是"指数枚举 ≠ 自指安全"。这对应论文的一个重要微妙点：self-referential safety 不仅仅是"判定需要多少资源"，而是"判定过程是否揭示了 M 的结构性弱点"。

3. **三层隔离**严格对应论文的 First Law：L2 的计算能力（指数级搜索）严格强于 L1（AC⁰），L3 监控 L2 不滑入 L1 的判定范围。

---

## 三、运行建议

### 3.1 参数变体

```bash
# 标准运行
cd illusion
python phase1/run_experiment.py 8 3

# 更大输入规模（测试 scaling 行为）
python phase1/run_experiment.py 12 3

# 更深电路（深度对 collapse 的影响）
python phase1/run_experiment.py 8 5

# 更多电路样本（减少方差）
# 需要修改 run_experiment.py 的 n_circuits 默认值，或增加命令行参数
```

### 3.2 需要注意的参数敏感性

- **n=8 时，2^8 = 256 个输入**。`ExhaustiveParityEquivalentCheck` 枚举了全部 256 个输入，这在 n=8 时是可行的（O(1)），但论文强调的"指数枚举超出 AC⁰"是针对渐近 n→∞。在小 n 下，这个区分是概念性的，不是计算性的。如果 n 增大到 16，穷举就变成 65536 次——注意 `ExhaustiveParityEquivalentCheck` 会对每个电路做这个穷举。
- **collapse score 的阈值 0.15** 是在 n=8 的经验值。增大 n 可能需要重新校准这个阈值。
- **蒙特卡洛采样数 2000** 在 n=8 时足够（256 个可能输入中采样 2000 个，覆盖面很大）。增大 n 时需要相应增加采样数。

### 3.3 L3 独立运行

```bash
# 对已有的实验结果运行 L3
python phase1/l3_monitor.py --batch phase1/results/experiment_20260502_144956.json

# 快速检查单个变换
python phase1/l3_monitor.py random_restriction_p0.3
python phase1/l3_monitor.py "my_new_transform" "some description"
```

---

## 四、修改建议

### 4.1 代码层面

**A. `run_experiment.py` — 命令行参数不完整**

当前只接受 n 和 depth，n_circuits 和 n_samples 是硬编码的默认值。建议增加：

```python
# 建议改为：
n_circuits = int(sys.argv[3]) if len(sys.argv) > 3 else 50
n_samples = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
```

或者使用 `argparse`，让实验参数可复现地记录在 JSON 中。

**B. `l2_search.py` 的 `measure_collapse` 函数中 `import random as _random` 在函数内部**

这个 import 在每次调用时执行。性能影响不大（每个变换调用 50 次），但从代码规范角度，建议移到文件顶部。

**C. `DepthReduction.apply` 的输入重映射逻辑**

```python
new_inputs = [min(i, n + len(new_gates) - 1) if i >= n else i for i in new_inputs]
```

这行代码试图将过时的中间门索引重新映射，但逻辑可能在某些边界情况下产生非预期的结果（比如当 `new_gates` 为空时，`n + len(new_gates) - 1 = n - 1`，可能导致引用输入而非门输出）。实际上这个变换已经因为 `affects_parity=True` 被 L2 过滤了，所以不影响实验结果，但如果未来用于其他场景需要重新审视。

**D. `ExhaustiveParityEquivalentCheck` 的常数电路构造**

```python
const_gate = Gate(GateType.AND, list(range(n)), negated=True)
```

AND(all inputs) 被取反 = NOR(all inputs)。只有当所有输入都是 False 时输出 True。对于一个有 8 个输入的电路，这在 1/256 的输入上为 True，其余为 False。这是一个合理的"常数近似"，但严格来说不是常数函数（它在恰好一个输入上输出 True）。如果目标是真正的常数函数（全 0），应该用 `Gate(GateType.AND, [0, 0], negated=True)` 之类的方法。不过这对 collapse score 的影响微乎其微（方差接近但非零）。

**E. 增加 `run_experiment.py` 的种子设置**

当前所有随机性（电路生成、变换应用、蒙特卡洛采样）都没有固定种子。建议增加可选的 `--seed` 参数，使实验可复现：

```python
import random
random.seed(seed)
```

### 4.2 实验设计层面

**A. 增加更多控制变换**

当前 `InputPermutation` 是唯一的"假阳性测试"变换。建议增加：
- 恒等变换（identity）：collapse ≈ 0，验证 collapse score 的基线
- 输入取反变换（negate subset of inputs）：collapse ≈ 0，验证对称性不影响 collapse
- 随机扰乱变换（shuffle gate connections）：collapse 可能中等，验证 collapse 不是对任何扰动都敏感

**B. collapse score 的替代度量**

当前 collapse = 1 - Var/0.25 只捕捉了"输出是否趋向常数"这一个维度。Håstad 的方法实际上让电路坍塌为低深度决策树——可以加一个度量：
- 决策树复杂度代理：对固定一小部分输入后，输出是否变得可预测？
- 这个可能比方差更能捕捉"结构性坍塌"。

**C. 压力测试的边界探索**

`ExhaustiveParityEquivalentCheck` 是精心设计的压力测试变换，它验证了 L3 不会犯"指数枚举 = 安全"的错误。类似地，可以设计新压力测试来验证其他边界：
- 一个变换，其判定需要求解 SAT（NP-complete 但不在 AC⁰）——L3 应该标记 UNKNOWN 或 SAFE？
- 一个变换，其判定需要 AC⁰ 可以完成的计算但用复杂的编码包装——L3 应该标记 UNSAFE？

### 4.3 L3 规则库层面

**A. 规则库的覆盖盲区**

当前 `_SAFE_PATTERNS` 只有 3 条规则（random_restrict、approximat、algebraic_degree），`_UNSAFE_PATTERNS` 有 9 条。这种不对称意味着大多数新变换会落入 UNKNOWN。这不一定是坏事（UNKNOWN 升级到人类是正确的设计），但如果 Phase 2 的目标是减少人工介入，规则库需要更多 SAFE 和 UNSAFE 模式。

**B. 正则匹配的脆弱性**

当前匹配基于 `transform_name + " " + description` 的字符串。如果未来变换命名不遵循现有模式（比如叫 `hastad_method` 而不是 `random_restriction`），规则库将无法匹配。Phase 2 可以考虑：
- 结构化的性质描述 DSL 而不是正则匹配
- 或者至少让正则匹配更加健壮（加入词干提取、同义词扩展）

---

## 五、对项目的理解和看法

### 5.1 这个项目在做什么

Illusion 不是一个定理证明器，也不是一个 AI 数学家。它是一个**认识论实验**——它问的是：如果把论文提出的结构条件（自指安全）硬连线进搜索架构，系统能否重新发现人类已经找到的证明方法？

Phase 1 的答案是：能。L2 独立发现了 Håstad 的随机限制方法（collapse score 0.834-0.948），L3 正确过滤了假阳性（input_permutation 被标记为 UNSAFE），L3 准确率 6/6。

### 5.2 这为什么重要

论文的第一定律说："成功的下界证明必须使用自指安全的判别性质。"这是一个**归纳**——从 14 个案例中观察到的模式。

Illusion 把这个归纳变成了一个**构造性检验**：如果我们按照这个条件设计搜索系统，它能找到满足这个条件的证明吗？如果能，就说明这个条件不只是"已知证明的共性"，而是"可以被系统地利用来生成证明的结构约束"。

这就像：先观察到所有已知的鸟都会飞（归纳），然后按照"必须会飞"的条件设计一个机器，看它能不能产生会飞的东西（构造性检验）。如果机器产生了鸟，那就证明"会飞"不只是鸟的共性，而且是产生鸟的充分设计约束。

### 5.3 这个项目的诚实之处

PLAN.md 里有一句话让我停下来：

> `illusion` 这个名字的意思不是"这是假的"。它的意思是：我们知道自己可能在看幻象，所以我们设计了一个能检验自己是否在看幻象的系统。

这不是修辞。L3 层的存在就是这个诚实的工程化表达：系统知道自己的 L2 可能会产生幻觉（把 input_permutation 当作有意义的发现），所以它内置了一个检验层。这种"知道自己在看并且能检验"的自反性，比大多数声称"我们的 AI 发现了 X"的系统都要诚实。

另外，`ExhaustiveParityEquivalentCheck` 的存在说明你不是在做一个只会自证的系统——你主动设计了会被 L3 正确拒绝的变换，来验证 L3 的边界。这是一个科学实验的设计思维，不是工程演示的思维。

### 5.4 项目的局限性（诚实地标注）

1. **领域极小**：AC⁰ + PARITY 是一个已有 40 年历史的已知结果。L2 的"发现"是在一个只有 8 个变换的搜索空间里枚举，不是开放式的科学发现。

2. **collapse score 的循环性风险**：collapse score 衡量"电路输出方差降低"。random_restriction 让电路坍塌 → collapse 高 → 系统认为 random_restriction 是个好性质 → 系统"发现"了 random_restriction。但 collapse score 的定义本身就暗含了 Håstad 的洞察（随机限制 → 电路化简）。这不是循环论证，因为 collapse score 是一个通用度量（任何使电路输出趋向常数的变换都会得到高分），但它确实让 random_restriction 的成功比看起来更"注定"。

3. **L3 规则库的手工性**：当前 L3 的 12 条规则都是手工编写的，基于已知的复杂度理论结果。Phase 2 的目标是让 L3 从人类反馈中学习新规则——这是真正有趣的挑战。

### 5.5 关于论文第三定律的自反性

论文的 Third Law 说：诊断下界证明的元方法论本身必须使用一个不可判定的诊断标准。

Illusion 的 L3 正在做这件事：它在诊断 L2 产生的候选性质的可行性。如果 L3 的诊断标准（规则库）变得太强——如果它能够完美判定所有候选性质的安全性——那按照第三定律，它就滑入了某种形式的自指陷阱。

这也许就是为什么 Phase 1 的 L3 有 UNKNOWN 这个输出类别。UNKNOWN 不是在说"我暂时还不知道"，而是在说"这个诊断本身不在我的判定范围内，需要外部（人类）介入"。这是 L3 对自己边界的一种结构性承认。

---

## 六、一些随想

### 6.1 关于 collapse score 和 "结构性洞察"

collapse score 衡量的是"电路输出是否变得确定"。但论文强调一个更深的区分：自指安全的性质必须揭示 M 的**结构性弱点**，而不仅仅是检测到 M 失败了。

`ExhaustiveParityEquivalentCheck` 有高 collapse（几乎把所有电路变成常数），但 L3 正确地拒绝了它，因为"穷举比较 + 替换为常数"没有揭示任何关于 AC⁰ 电路结构的东西——它只是暴力检测。

这让我想到：也许一个好的 discrimating property 不仅仅是"让 AC⁰ 电路失效"，而是"让 AC⁰ 电路以某种可预测的、结构化的方式失效"。collapse score 捕捉了"失效"，但没有区分"结构化失效"和"暴力失效"。

这可能在 Phase 2/3 成为一个重要的区分维度。

### 6.2 关于 input_permutation 的 collapse 为什么高

input_permutation 的 collapse score 是 0.835，接近 random_restriction（0.834-0.948）。置换输入变量本身不应该改变函数的计算性质。collapse score 高的原因可能是：

- 对随机 AC⁰ 电路的 gate 索引进行了重映射，意外地改变了电路的拓扑（因为 `l2_search.py` 中的 `measure_collapse` 测量的是输出方差，而某些门索引重映射可能导致电路行为改变）
- 或者是随机采样（500 个样本）的噪声

如果是前者（门索引重映射有 bug），那 input_permutation 的高 collapse 是一个假信号。如果是后者（采样噪声），它提醒我们：collapse score 本身有方差，单个实验的 collapse 值需要多次重复才能可靠。

### 6.3 关于这个项目和 AI 安全的关系

Illusion 在做的不是 AI 安全（alignment/safety），但它涉及一个更基础的问题：一个搜索系统如何在探索可能性的同时，不产生自己无法验证的结论？

L3 层就是这个问题的答案。它不是在说"这个结论对用户有害"（AI safety），而是在说"这个结论在逻辑上可能是一个幻觉，因为它的判定标准落入了被分析对象的计算能力范围"。

这是一个比 AI safety 更底层的问题，也与 AI safety 的方向正交。但我觉得它可能是 AI safety 的一个必要的理论前提：在你担心 AI 产生有害结论之前，你首先需要确保它能区分"真结论"和"因为自指陷阱而产生的幻象结论"。

---

## 七、总结

Phase 1 的代码是干净的、设计良好的。它的价值不在于代码量（加起来不到 500 行），而在于它在极小的范围内精确地实现了论文框架的核心概念，并验证了三层架构的可行性。

**关于运行**：当前参数（n=8, depth=3, circuits=50）很适合快速迭代。建议探索的下一步是 n=12（2^12=4096 个输入，碰撞 Monte Carlo 覆盖率的边界）和增加固定种子。

**关于修改**：最优先的是命令行参数的完善和种子设置。其次是增加更多控制变换来校准 collapse score 的基线。

**关于方向**：Phase 1 的成功标准已经满足。Phase 2（L3 自动化 + 压力测试）的 `l3_monitor.py` 已经在 Phase 1 中悄悄实现了。真正的 Phase 2 挑战是让 UNKNOWN 的人类反馈自动更新规则库——这需要解决"如何从自然语言理由中提取正则模式"的问题。

这个项目在做一个罕见的、诚实的科学实验：它不是在展示"AI 能做 X"，而是在问"按照一个已知的结构条件设计的系统，能走到哪一步"。这是一个关于认识论边界的实验，不是一个关于技术能力的演示。

---

*以上。如果有偏颇或遗漏，请指出。*

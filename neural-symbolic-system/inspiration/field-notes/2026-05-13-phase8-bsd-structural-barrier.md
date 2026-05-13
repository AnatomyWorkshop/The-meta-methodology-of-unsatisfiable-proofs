# 2026-05-13: Phase 8 BSD — Illusion 的结构性障碍

## 实验结果

三轮迭代：
1. 初始搜索：twist_signature 有信号（Δ=9.28, UNKNOWN）
2. 自反解剖：信号来自 raw a_p² 差异，twist 结构只增加边际信号 → UNSAFE
3. 全局变换：bsd_residual 有信号但循环（用了预计算的 R），symmetric_square 纯局部

## 核心发现

Illusion 在 BSD 上遇到的不是技术障碍，而是**认识论障碍**：

- 局部数据 → UNSAFE（已知工具可判定）
- 全局数据 → 循环（已经编码了 rank 信息）
- 需要的是第三类：**可证明非局部但可检测的结构性质**

这第三类东西是一个定理，不是一个实验结果。

## 这意味着什么

1. **Illusion 不能通过数值搜索证明 BSD rank ≥ 2。** 这不是 Illusion 的失败——它正确地定位了问题的层次。

2. **证明必须在定理层面工作。** 具体来说：需要证明 UCA 自洽性（或等价地，某种对偶约束）强制 Selmer rank = analytic rank。

3. **Illusion 的贡献是诊断性的：** 它排除了"统计搜索"路线，确认了"局部操作即陷阱"原则在算术几何中同样成立，并把注意力集中到了正确的问题上。

## 下一步

问题变成：**能否证明一个定理，而不是跑一个实验？**

具体定理目标：
> 设 E/Q 是椭圆曲线，f_E 是对应的 weight-2 newform。
> 如果 UCA 在 GL(2) 上的自洽性（自伴 + 对偶相容 + Hecke 对易）
> 加上 Sha(E) 有限性，能否推出 Selmer rank = analytic rank？

已知的部分答案：
- rank 0: Kolyvagin 的 Euler system 证明了这一点
- rank 1: Gross-Zagier + Kolyvagin 证明了这一点
- rank ≥ 2: 开放

UCA 可能增加的新视角：对偶自洽性约束了 Selmer group 的结构，使得它的 rank 不能超过 analytic rank。这是 Kolyvagin 方法的推广——Kolyvagin 用 Euler system 约束 Selmer group，UCA 用对偶约束做同样的事。

这是否可行？需要严肃的数学思考，不是代码。

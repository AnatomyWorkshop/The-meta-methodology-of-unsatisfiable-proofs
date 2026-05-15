这版其实已经比前面健康很多了。

你已经修掉了几个真正危险的问题：

* routing 单一来源
* LiteLLM 接入
* 全局递归深度
* trace logging
* protocol schema

这些已经从“实验脚本”进入：

> “初代 runtime”

阶段了。

现在剩下的技术债，
已经不再是“明显错误”，而是：

# 架构演化债（evolution debt）

也就是说：

现在还能跑，
但未来规模一扩大就会卡死。

我按严重程度说。

---

# 1. 最大技术债：dispatch 还不是真正的 Runtime

现在：

```python
dispatch()
```

仍然承担了：

* routing
* context assembly
* model execution
* trace logging
* op execution
* recursion management

几乎所有事情。

这意味着：

# dispatch 已经开始变成 God Function。

虽然现在还能控制。

但你已经能看到：

```python
dispatch(..., auto_execute=True)
```

这种“隐式行为增长”了。

---

未来一定会出现：

```text
before_dispatch
after_dispatch
middleware
retry
memory retrieval
policy evaluation
caching
```

然后：

dispatch 会变成 2000 行。

---

## 现在最该做的

不是拆文件。

而是：

# 引入 DispatchContext / DispatchResult

例如：

```python
ctx = DispatchContext(...)
```

然后：

```python
Runtime.dispatch(ctx)
```

因为：

你们已经不是：

```python
query -> response
```

而是：

# “认知状态流”

了。

---

# 2. Trace 系统还不够“可重放”

你现在：

```python
context_hash
task_preview
```

已经很好了。

但：

# replay 仍然不可能。

因为缺：

---

## （A）完整 system prompt

你现在只存 hash。

未来 debugging：

会很痛苦。

---

## （B）model snapshot

例如：

```text
claude-sonnet-4-20250514
```

还不够。

因为：

provider 行为会漂移。

---

## （C）routing decision trace

未来：

你会需要：

```json
{
  "reason": "task_type=judgment → claude"
}
```

否则：

自动 policy 后：

根本无法解释。

---

## （D）parent trace

你现在：

recursive dispatch：

还没有：

```text
parent_trace_id
```

未来：

debug recursive cognition 会崩溃。

---

# 3. execute_ops() 还是同步阻塞模型

这是未来很大的问题。

例如：

```text
@diagnose target=rh
```

可能跑：

300秒。

但：

现在：

dispatch 会卡死。

---

未来：

你们必须：

# op queue 化。

例如：

```text
dispatch
↓
emit operation
↓
runtime scheduler
↓
async execution
```

否则：

复杂 workflow 会完全阻塞。

---

尤其：

你们未来天然会走向：

# long-running cognition

不是普通聊天。

---

# 4. @op 参数解析非常脆弱

现在：

```python
parts[1].split()
```

是：

# prototype parser。

例如：

```text
@dispatch task="analyze RH barrier"
```

现在会炸。

因为：

空格断裂。

---

你们未来必须：

# 正式 DSL 化。

至少：

```text
@dispatch {"task":"..."}
```

或者：

```yaml
@dispatch
task: ...
```

---

因为：

现在：

协议已经开始成为：

# 系统核心。

不能再：

string split。

---

# 5. Capability System 还不存在

这是未来最危险的。

例如：

现在：

```text
@archive path=...
```

模型直接有：

filesystem authority。

---

未来：

你们会出现：

```text
@dispatch recursion bomb
```

或者：

```text
@archive ../../
```

这种问题。

---

现在虽然：

prototype 阶段问题不大。

但：

# 一旦 Web 化会非常危险。

---

我建议：

现在就开始：

```python
ctx["capabilities"] = {...}
```

例如：

```python
{
  "allow_dispatch": True,
  "allow_archive": False
}
```

---

# 6. Prompt Variant 仍然是“文本后缀”

这是很大的隐藏债。

你们现在：

```python
system_suffix
```

其实只是：

# prompt patching。

---

但你们已经开始：

A/B cognition。

未来：

variant 会变成：

# policy graph。

例如：

```yaml
verbosity: high
aggression: low
formalism: medium
skepticism: high
```

然后：

动态组合。

---

否则：

variant 数量会指数爆炸：

```text
default
concise
concise_critical
concise_critical_formal
...
```

最后不可维护。

---

# 7. adversarial() 仍然只是文本循环

这是目前：

# 最大认知层技术债。

因为：

critic 没有：

* issue memory
* contradiction tracking
* resolved issue state

所以：

现在：

本质还是：

```text
LLM chat ping-pong
```

而不是：

# structured debate。

---

未来：

你们会需要：

```python
IssueGraph
```

例如：

```json
{
  "issue_id": "...",
  "status": "resolved",
  "introduced_by": "critic",
  "addressed_in": "round3"
}
```

---

否则：

系统会：

* 重复 critique
* 忘记历史
* pseudo-convergence

---

# 8. Batch 系统没有真正的任务状态机

现在：

```text
.done
```

已经不错。

但：

未来：

你们需要：

```text
pending
running
retrying
failed
blocked
completed
```

因为：

long-running agent 一定会需要恢复。

---

# 9. 缺少“观察层”

这是很容易被忽略的。

你们现在：

只有：

```text
task -> model -> result
```

但未来：

runtime 真正重要的是：

# introspection。

例如：

* 为什么选这个模型？
* 为什么判定 converge？
* 为什么 dispatch？
* 为什么 retry？

---

也就是：

# reasoning about reasoning。

---

# 10. 最深层技术债

也是我认为最关键的：

# “task_type” 还是人工 taxonomy

例如：

```python
judgment
critique
analysis
```

这是：

# 人类静态分类。

---

但未来：

你们真正会需要：

# latent cognition routing。

例如：

```text
需要：
高创造性 + 高批判性 + 长上下文
```

自动映射：

```text
claude + adversarial + deep_context
```

---

也就是说：

现在：

```text
task_type
```

还是：

# symbolic routing。

未来：

你们会进入：

# semantic routing。

---

# 总结

你们已经从：

```text
prompt engineering
```

进入：

# runtime engineering

了。

现在最大的技术债已经不是：

* yaml
* parser
* 文件拆分

这种表层问题。

而是：

# “认知状态管理”

包括：

| 层级        | 核心债                     |
| --------- | ----------------------- |
| Runtime   | dispatch god function   |
| Protocol  | string-based op parsing |
| Security  | capability system 缺失    |
| Cognition | issue graph 缺失          |
| Tracing   | 不可 replay               |
| Variants  | prompt topology 未结构化    |
| Routing   | 仍是 symbolic task type   |
| Execution | 同步阻塞 op                 |

这些债，
其实已经说明：

你们开始接近：

# “真正 Agent Runtime”

会遇到的问题了。

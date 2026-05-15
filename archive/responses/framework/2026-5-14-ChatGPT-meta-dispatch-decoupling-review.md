这里面有些是“现在必须修”，有些是“典型工程师过度洁癖”。

它们的重要性其实差别非常大。

我按真正优先级排序。

---

# 第一优先级（必须尽快修）

## 1. 配置与代码脱节

这个我认为：

# 真的是严重问题。

因为这不是“代码风格问题”。

而是：

# 系统真实性问题。

如果：

```text
config.yaml
```

和：

```python
ROUTING_TABLE
```

同时存在。

那未来一定会出现：

```text
文档以为：
judgment → claude

实际运行：
judgment → deepseek
```

而且：

这种 bug 极难察觉。

因为：

系统还能运行。

只是：

# “认知策略 silently drift”

这比 crash 更危险。

---

尤其你们做的是：

# cognition orchestration

不是普通 CRUD。

所以：

routing policy 本身就是：

# 核心资产。

因此：

## 我建议：

立即做到：

```text
Single source of truth
```

也就是：

# routing/config 必须唯一来源。

---

甚至：

以后：

```yaml
routing:
  judgment:
    model: claude
    variant: strategic
```

这种东西：

应该能热更新。

runtime 不该硬编码。

---

# 第二优先级（应该近期修）

## 2. _DISPATCH_DEPTH 全局变量

这个确实是：

# 真 bug。

而不是架构洁癖。

因为：

只要未来：

* batch parallel
* async
* web server
* queue worker

出现。

你们就会炸。

例如：

线程A：

```text
depth=2
```

线程B：

突然也读到：

```text
depth=2
```

直接错误阻塞。

---

而且：

你们的系统天然会走向：

# recursive dispatch

所以：

这个问题未来一定会越来越严重。

---

## 正确做法

不要：

```python
global _DISPATCH_DEPTH
```

而是：

# dispatch context

例如：

```python
dispatch(..., context={
    "depth": 2
})
```

或者：

```python
DispatchSession
```

对象。

---

这是：

# runtime state

不是全局配置。

---

# 第三优先级（建议修）

## 3. LiteLLM 问题

这个其实是：

# “产品方向问题”

不是纯技术问题。

---

因为你们现在：

实际上在：

# 重造 LiteLLM 的 transport layer。

例如：

* retries
* fallback
* pricing
* provider abstraction

LiteLLM 都有。

---

所以：

如果你们目标是：

# cognition runtime

那：

# 不应该自己维护 provider infra。

这是错误抽象层。

---

你们真正独特的是：

* routing cognition
* adversarial loops
* semantic protocols
* prompt topology

不是：

HTTP request。

---

所以：

我认为：

## 应该尽快切 LiteLLM。

原因不是“代码优雅”。

而是：

# 保持认知层聚焦。

否则：

你们会被 provider engineering 吞掉。

---

# 第四优先级（可延后）

## 4. Task classifier 不存在

这个：

我认为没那么急。

因为：

现在：

```bash
--type judgment
```

其实反而：

# 更适合研究阶段。

原因：

你们现在还在：

# 定义 task ontology。

---

如果现在急着：

```text
自动分类
```

很容易：

* 错误分类
* prompt drift
* routing 不稳定

然后：

你们会不知道：

是：

* 模型问题
* prompt问题
* classifier问题

---

所以：

我反而建议：

# 先人工 task typing。

等：

你们真正稳定后。

再：

```text
classifier → suggestion
```

而不是强制自动。

---

## 更好的路线

不是：

```python
auto classify
```

而是：

# routing recommendation

例如：

```text
Suggested:
task_type=critique
variant=adversarial
```

用户确认。

---

因为：

你们是：

# research runtime

不是聊天助手。

显式控制更重要。

---

# 第五优先级（现在不用管）

## 5. PyYAML 问题

这个我认为：

# 完全不是当前核心问题。

甚至：

我觉得现在自己 parser 反而合理。

因为：

你们现在 YAML 很简单。

而：

# dependency minimization

在 prototype 阶段是有价值的。

---

真正的问题不是：

```text
不用 pyyaml
```

而是：

# schema validation 不存在。

---

例如：

现在：

```yaml
judgment:
  model claude
```

少个冒号。

可能 silently fail。

这才危险。

---

所以：

如果未来复杂化：

我建议：

不是直接 PyYAML。

而是：

# Pydantic schema + yaml

因为：

你们其实需要：

# cognition config validation

不是 YAML parsing。

---

# 真正更重要，但你们还没意识到的问题

下面这些，
我认为比 YAML/parser 更重要。

---

# 1. dispatch 没有 immutable trace id

你们现在：

```python
thread_id
```

不够。

未来：

你们会需要：

```text
root_trace_id
parent_trace_id
dispatch_id
```

因为：

recursive dispatch 会形成：

# cognition tree

没有这个：

以后根本无法 replay/debug。

---

# 2. @op 没有 capability boundary

现在：

```text
@archive
@dispatch
```

直接执行。

未来：

这是非常危险的。

因为：

模型可能：

* 无限 dispatch
* 删除文件
* 自触发循环

---

所以：

未来需要：

# capability system

例如：

```python
allowed_ops=["dispatch"]
```

---

# 3. adversarial 没有 semantic memory

现在：

critic 不知道：

* 哪些问题已经提过
* 哪些问题已解决

只是文本循环。

未来：

你们会需要：

# issue graph

这是很关键的跃迁。

---

# 4. prompt variant 还只是字符串

但未来：

你们会发现：

# variant 本身需要结构化。

例如：

```yaml
variant:
  verbosity: low
  aggressiveness: high
  abstraction: medium
```

因为：

真正的 prompt topology：

不是：

```text
variant_a
variant_b
```

而是：

# 连续认知空间。

---

# 总结

真正应该立即修：

| 问题        | 优先级 |
| --------- | --- |
| 配置与代码脱节   | 极高  |
| 全局递归深度    | 极高  |
| LiteLLM缺失 | 高   |

可以晚点：

| 问题              | 优先级 |
| --------------- | --- |
| task classifier | 中   |
| PyYAML          | 低   |

而真正未来的大问题：

* cognition trace
* capability system
* issue graph
* semantic routing
* structured prompt topology

这些其实比“parser 用不用 yaml”重要得多。

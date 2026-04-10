---
title: AutoGen
description: Microsoft 的多 Agent 对话框架，将 Agent 间协作建模为结构化对话。
created: 2026-04-10
updated: 2026-04-10
tags: [framework, microsoft, agent, python, multi-agent]
review:
---

# AutoGen

> Microsoft 出品，核心思路是将多 Agent 协作建模为**结构化对话**——Agent 之间通过消息传递协作，而非函数调用。

| 属性 | 值 |
|------|-----|
| 厂商 | Microsoft |
| 语言 | Python |
| 开源 | 是 |
| GitHub | [microsoft/autogen](https://github.com/microsoft/autogen) |
| 官网 | [microsoft.github.io/autogen](https://microsoft.github.io/autogen/)[^autogen-docs] |

## 技术亮点

- **对话即协作**：Agent 间交互不是 RPC 调用，而是异步消息流。每个 Agent 维护自己的上下文和推理循环，通过发送/接收消息与其他 Agent 协作。这种设计天然适合需要多轮讨论、意见汇总的场景（如代码审查：Coder Agent 写代码 → Reviewer Agent 提意见 → Coder Agent 修改）
- **GroupChat 模式**：多个 Agent 在一个共享对话中协作，由 GroupChatManager 控制发言顺序（轮询、模型选择、自定义逻辑）。相比简单的链式调用，GroupChat 允许 Agent 动态决定谁来回应当前问题
- **人类参与（Human-in-the-loop）**：`UserProxyAgent` 将人类作为对话中的一个参与者，Agent 可以在关键节点请求人类输入、确认或纠正

## 参考资料

[^autogen-docs]: Microsoft. *AutoGen Documentation*. https://microsoft.github.io/autogen/

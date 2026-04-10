---
title: LangGraph
description: LangChain 团队出品的图驱动 Agent 编排框架，用有向图建模 Agent 工作流。
created: 2026-04-10
updated: 2026-04-10
tags: [framework, langchain, agent, python, javascript]
review:
---

# LangGraph

> LangChain 团队出品，用**有向图**（而非线性链）建模 Agent 工作流——节点是计算步骤，边是状态转移。

| 属性 | 值 |
|------|-----|
| 厂商 | LangChain |
| 语言 | Python / JavaScript |
| 开源 | 是 |
| GitHub | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| 官网 | [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)[^langgraph-docs] |

## 技术亮点

- **图即工作流**：Agent 的执行逻辑表达为 `StateGraph`——节点是函数（agent 推理、工具调用、人类审批等），边定义状态转移和条件分支。相比线性 Chain，图天然支持循环、分支、并行，直接对应 [ReAct 循环](../applied/ai-agents.md)的 Think→Act→Observe→Think 回路
- **状态持久化（Checkpointing）**：每个节点执行后自动保存图状态快照，支持断点恢复、时间旅行（回退到任意历史节点）、人机交互中断与继续。这是 long-running Agent 的关键基础设施
- **LangChain 生态集成**：与 LangChain 的模型抽象、工具接口、向量存储无缝集成，可复用 LangChain 生态中的大量现成组件

## 与 LangChain 的关系

LangChain 是组件库（模型、工具、检索器等标准抽象），LangGraph 是编排层（定义这些组件如何协作）。LangChain 提供"零件"，LangGraph 提供"装配图"。

## 参考资料

[^langgraph-docs]: LangChain. *LangGraph Documentation*. https://langchain-ai.github.io/langgraph/

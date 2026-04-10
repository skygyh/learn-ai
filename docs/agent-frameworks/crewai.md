---
title: CrewAI
description: 角色驱动的 Agent 团队框架，用"角色—目标—背景故事"三元组定义 Agent 个性。
created: 2026-04-10
updated: 2026-04-10
tags: [framework, crewai, agent, python, multi-agent]
review:
---

# CrewAI

> 角色驱动的 Agent 团队框架——每个 Agent 有明确的**角色、目标、背景故事**，像组建一支团队一样编排多 Agent 协作。

| 属性 | 值 |
|------|-----|
| 厂商 | CrewAI |
| 语言 | Python |
| 开源 | 是 |
| GitHub | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| 官网 | [crewai.com](https://www.crewai.com/)[^crewai-docs] |

## 技术亮点

- **角色三元组**：每个 Agent 用 `(role, goal, backstory)` 定义——role 是身份标签，goal 是任务目标，backstory 是角色背景。三元组作为 system prompt 的一部分注入，引导模型以该角色的视角和风格行动。简单但有效地解决了"多个 Agent 行为趋同"的问题
- **两种执行模式**：Sequential（管道式，任务按顺序传递）和 Hierarchical（层级式，Manager Agent 分配任务给 Worker Agent）。对应 [AI Agent 智能体 § 从单循环到多循环](../applied/ai-agents.md)中的管道式和层级式模式
- **任务委派（Delegation）**：Agent 可以主动将任务委派给团队中更适合的 Agent，由框架自动路由。这模拟了真实团队中的"这个问题你更擅长，交给你"

## 参考资料

[^crewai-docs]: CrewAI. *CrewAI Documentation*. https://docs.crewai.com/

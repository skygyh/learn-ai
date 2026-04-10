---
title: Semantic Kernel
description: Microsoft 的企业级 AI 编排 SDK，以 Plugin 架构桥接 AI 能力与企业已有系统。
created: 2026-04-10
updated: 2026-04-10
tags: [framework, microsoft, agent, csharp, python, java, enterprise]
review:
---

# Semantic Kernel

> Microsoft 出品的企业级 AI 编排 SDK，核心定位是**桥接 AI 能力与企业已有系统**——用 Plugin 封装企业逻辑，用 Planner 自动编排。

| 属性 | 值 |
|------|-----|
| 厂商 | Microsoft |
| 语言 | C# / Python / Java |
| 开源 | 是 |
| GitHub | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) |
| 官网 | [learn.microsoft.com/semantic-kernel](https://learn.microsoft.com/en-us/semantic-kernel/)[^sk-docs] |

## 技术亮点

- **Plugin 架构**：将企业已有的函数、API、服务封装为 Plugin（语义函数 + 原生函数），AI 模型通过函数描述自动发现和调用。设计哲学是"AI 适配企业系统"而非"企业围绕 AI 重写"
- **多语言 SDK**：同时支持 C#、Python、Java，且 API 设计保持一致。这是唯一认真覆盖 .NET 和 Java 生态的 Agent 框架，对企业技术栈的兼容性远超 Python-only 的竞品
- **Azure 深度集成**：与 Azure OpenAI Service、Azure AI Search、Microsoft 365 原生集成，在微软企业生态中的部署摩擦最小

## 参考资料

[^sk-docs]: Microsoft. *Semantic Kernel Documentation*. https://learn.microsoft.com/en-us/semantic-kernel/

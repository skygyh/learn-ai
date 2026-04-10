---
title: Dify
description: 开源的可视化 AI 应用开发平台，用拖拽式界面构建 Agent 和 RAG 工作流。
created: 2026-04-10
updated: 2026-04-10
tags: [framework, dify, agent, python, low-code]
review:
---

# Dify

> 开源可视化 AI 应用平台——用拖拽式界面构建 Agent 和 RAG 工作流，降低 AI 应用的开发门槛。

| 属性 | 值 |
|------|-----|
| 厂商 | Dify |
| 语言 | Python / TypeScript |
| 开源 | 是 |
| GitHub | [langgenius/dify](https://github.com/langgenius/dify) |
| 官网 | [dify.ai](https://dify.ai/)[^dify-docs] |

## 技术亮点

- **可视化工作流编排**：通过 Web UI 拖拽节点构建 Agent 工作流（LLM 调用、条件分支、工具调用、代码执行），无需写代码即可组装复杂流程。适合快速原型验证和非工程背景用户
- **内置 RAG 管线**：平台内集成文档上传、分块、嵌入、向量存储和检索全流程，与 Agent 工作流无缝衔接。省去自建 [RAG](../applied/rag.md) 基础设施的工程量
- **Backend-as-a-Service**：构建的应用直接暴露 API 端点，可作为后端服务集成到现有系统中

## 参考资料

[^dify-docs]: Dify. *Dify Documentation*. https://docs.dify.ai/

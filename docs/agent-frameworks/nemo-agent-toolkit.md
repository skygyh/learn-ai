---
title: NeMo Agent Toolkit
description: NVIDIA 的跨框架 Agent 元工具包——可观测性、安全沙箱、本地推理，解决"Agent 怎么安全运行和优化"的工程问题。
created: 2026-04-10
updated: 2026-04-10
tags: [framework, nvidia, agent, python, observability, security]
review:
---

# NeMo Agent Toolkit

> NVIDIA 出品，定位不是"又一个 Agent 框架"，而是坐在 LangChain/CrewAI 之上的**元框架**——解决"Agent 怎么安全运行、跨框架优化"的工程问题。

| 属性 | 值 |
|------|-----|
| 厂商 | NVIDIA |
| 语言 | Python |
| 开源 | 是 |
| GitHub | [NVIDIA/NeMo-Agent-Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) |

## 技术亮点

- **Function-as-a-Service 统一抽象**[^nvidia-agent-toolkit]：将 Agent、工具、子 Agent、整个工作流统一抽象为 `fn(input) → output` 的可调用函数，无论底层是 LangChain、CrewAI 还是原生 Python 都表现为同一接口。这使得跨框架 Agent 系统的 **token 用量、延迟、成本** 可以在统一的 profiling 链路中追踪，工作流通过 YAML 配置组合，替换组件无需改代码

### OpenShell：Agent 安全运行时

核心问题：自主 Agent 拥有文件访问、网络请求、代码执行等能力，如何防止越权？OpenShell 的方案是**声明式策略驱动的沙箱**[^nvidia-openshell]：

- **策略文件**：Agent 在隔离容器中运行，通过策略文件声明允许的文件路径、网络出口、可调用的 API
- **推理路由**：将 API 调用透明路由到本地/自托管后端，避免敏感数据泄露到外部服务
- **OCSF 日志**：沙箱内所有 Agent 行为（文件操作、网络请求、推理调用）以 [OCSF](https://ocsf.io/) 标准格式记录，可对接企业安全信息系统
- 支持主流 Agent：Claude Code、Codex 等

### NemoClaw：参考栈

OpenShell 之上的一键启动方案[^nvidia-nemoclaw]，将 OpenClaw（always-on 助手 Agent）+ OpenShell（安全沙箱）+ Nemotron（开源推理模型）打包为完整栈：

```
NemoClaw（参考栈）
  ├── OpenClaw（always-on 助手 Agent）
  ├── OpenShell（安全沙箱 + 策略引擎）
  └── Nemotron（本地推理模型）
```

## 参考资料

[^nvidia-agent-toolkit]: NVIDIA. *NeMo Agent Toolkit*. https://github.com/NVIDIA/NeMo-Agent-Toolkit
[^nvidia-openshell]: NVIDIA. *OpenShell — Safe, private runtime for autonomous AI agents*. https://github.com/NVIDIA/OpenShell
[^nvidia-nemoclaw]: NVIDIA. *NemoClaw — Open source reference stack for always-on assistants*. https://github.com/NVIDIA/NemoClaw

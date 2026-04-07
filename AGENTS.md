# AGENTS.md — 项目约定

## 项目概述

个人 AI 前沿知识库。知识文档用中文编写，代码和配置用英文。

## 目录约定

- `docs/foundations/` — 基础理论（稳定知识，低频更新）
- `docs/applied/` — 应用技术（工程方法，中频更新）
- `docs/research/` — 前沿研究（快速演进，高频更新）
- `landscape/` — 行业全景（模型跟踪）
- `journal/YYYY/MM/DD.md` — 每日 RSS 原始素材（脚本自动生成）
- `resources.md` — 精选资源汇总
- `scripts/` — 自动化脚本

## Markdown 规范

- 所有知识文档必须有 YAML frontmatter（title, description, created, updated, tags）
- 日报用简化 frontmatter（date, type）
- 每次修改知识文档时更新 `updated` 字段
- 参考资料统一放在文档末尾的 `## 参考资料` 区

## 日更脚本

- 入口：`scripts/daily_update.py`
- 只做一件事：拉 RSS → 写 `journal/YYYY/MM/DD.md`
- 依赖管理：PEP 723 inline metadata，`uv run` 自动安装
- GitHub Actions：`.github/workflows/daily-update.yml`，每天 UTC 00:00 运行
- RSS 源在脚本顶部 `RSS_FEEDS` 列表中配置，只保留经过验证可用的源
- 运行：`uv run scripts/daily_update.py` 或 `uv run scripts/daily_update.py --hours 48`

## LLM 整理流程（手动触发）

脚本只负责拉取原始素材到 journal/。后续整理由人+LLM 协作完成：

### 1. 阅读当日素材

打开 `journal/YYYY/MM/DD.md`，浏览今日的原始条目。

### 2. 更新 landscape/model-tracker.md

如果有新模型发布或重大更新：
- 在对应的闭源/开源表格中添加新行
- 在 `## 最近更新` 下追加条目
- 更新 frontmatter 的 `updated` 字段

### 3. 更新知识文档

如果有值得纳入知识体系的内容，更新对应文件：

| 素材类型 | 归入文件 |
|----------|----------|
| 新模型架构/技术 | `docs/foundations/large-language-models.md` |
| 多模态新进展 | `docs/foundations/multimodal-ai.md` |
| 训练/对齐新方法 | `docs/foundations/training-and-alignment.md` |
| 提示技巧/框架 | `docs/applied/prompt-engineering.md` |
| RAG 新方法 | `docs/applied/rag.md` |
| Agent 框架/协议 | `docs/applied/agents.md` |
| 硬件/推理/部署 | `docs/applied/infrastructure.md` |
| 推理模型进展 | `docs/research/reasoning-and-planning.md` |
| 安全/治理/可解释性 | `docs/research/safety-and-governance.md` |
| 其他前沿方向 | `docs/research/emerging-frontiers.md` |

### 4. 更新 resources.md

如果发现值得长期收藏的论文、工具或博客，添加到 `resources.md` 对应分类下。

### 提示词参考

让 LLM 帮忙整理时可以这样说：

> 阅读 journal/2026/04/07.md 的今日素材，帮我：
> 1. 筛选出最值得关注的 5 条
> 2. 判断哪些应该更新到知识文档中
> 3. 直接帮我更新对应的文件（记得更新 frontmatter 的 updated 字段）

## 构建 & 验证

- 无构建步骤，纯 Markdown 仓库
- 日更脚本测试：`uv run scripts/daily_update.py --hours 1`

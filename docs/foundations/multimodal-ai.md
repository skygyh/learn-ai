---
title: "多模态 AI (Multimodal AI)"
description: "文本、图像、音频、视频四种模态的数据特征差异，以及各自的离散化、生成与跨模态对齐技术路线。"
created: 2026-04-07
updated: 2026-04-09
tags: [multimodal, vision-language, diffusion, audio, cross-modal-alignment]
review:
---

# 多模态 AI (Multimodal AI)

> 比较文本、图像、音频、视频四种核心模态的数据特征，以及 AI 处理它们的技术路线差异。

---

## 1. 模态特征一览

| 维度 | 文本 | 图像 | 音频 | 视频 |
|------|------|------|------|------|
| 数据结构 | 1D 离散序列 | 2D 连续网格 (H×W×C) | 1D 连续波形 | 3D (2D 空间 + 时间) |
| 信息密度 | 高——一个词承载大量语义 | 中——像素级冗余大 | 低——高采样率，有效信息稀疏 | 极低——帧间大量重复 |
| 天然离散性 | 是（词表有限） | 否（像素连续值） | 否（波形连续） | 否 |
| 典型序列长度 | ~10³–10⁴ tokens | ~10²–10³ patches | ~10³–10⁴ codec tokens | ~10⁴–10⁶ |
| 时间维度 | 无（或弱顺序） | 无 | 有，高分辨率 | 有，需帧间一致性 |

核心差异：文本天然离散、语义密度高；图像/音频/视频是连续信号，需要先**离散化**才能送入 Transformer，而离散化策略直接决定模型的效果上限。

---

## 2. 离散化：把连续信号变成 token

这是多模态 AI 最核心的技术问题——如何把不同模态统一到 Transformer 能处理的 token 序列。

### 文本

BPE / SentencePiece 等子词切分已是成熟方案，词表大小通常 32k–128k。文本是唯一**天然离散**的模态，无需额外编码。

### 图像

两条主路线：

| 路线 | 代表 | 原理 | 权衡 |
|------|------|------|------|
| Patch 嵌入 | ViT[^dosovitskiy-2020-vit] | 将图像切成 16×16 patch，线性投影为向量 | 简单高效，但 patch 粒度限制细节 |
| 离散码本 | VQ-VAE / VQ-GAN | 将图像编码为离散 token（码本索引） | 可用自回归生成，但码本大小限制保真度 |

实践中，**理解**任务多用 patch 嵌入（CLIP、Gemini），**生成**任务多用 VAE 潜空间 + 扩散模型。

### 音频

| 路线 | 代表 | 原理 |
|------|------|------|
| 频谱 → patch | Whisper, AST | 波形 → mel 频谱图（2D）→ 按 ViT 方式切 patch |
| 神经音频编码 | EnCodec, SoundStream | 将波形压缩为多层离散 token（残差向量量化, RVQ） |

音频的采样率问题：16kHz 语音 1 秒 = 16,000 个采样点，直接处理不现实。频谱图将时域转为时频域，大幅降低序列长度；神经编码则进一步压缩到 ~50–75 token/秒。

### 视频

视频 = 图像序列 + 时间轴，数据量爆炸。关键是如何压缩时间冗余：

- **帧采样 + 独立编码**：抽关键帧，每帧按图像处理——简单但丢失运动信息
- **3D patch**：将视频切成时空立方体（如 2 帧×16×16），一次编码空间+时间——Sora / DiT 的做法
- **时间维度单独建模**：图像编码后加 temporal attention 层

---

## 3. 生成技术路线

不同模态的生成方法差异很大，本质上由数据特征决定。

### 文本：自回归

逐 token 预测下一个，天然适配离散序列。Transformer decoder 是标准架构。

### 图像：扩散模型

自回归在连续高维空间效果不佳，扩散模型成为主流[^ho-2020-ddpm]：

```
前向：x₀ (清晰图) → 逐步加噪 → xₜ (纯噪声)
反向：xₜ (纯噪声) → 学习去噪 → x₀ (生成图)
```

关键改进：

- **Latent Diffusion**[^rombach-2022-ldm]：在 VAE 潜空间而非像素空间做扩散，计算量降低数十倍
- **DiT (Diffusion Transformer)**：用 Transformer 替代 UNet 作为去噪骨干，更好地 scale——Sora 的核心架构
- **Flow Matching**：更高效的采样路径，替代传统 DDPM 噪声调度

### 视频：扩散 + 时间一致性

在图像扩散基础上增加时间维度，但核心挑战不在生成质量而在**一致性**：

- 帧间对象连贯（同一个人不能变脸）
- 物理合理（重力、碰撞、流体）
- 镜头运动平滑

技术手段：3D 注意力（空间+时间联合 attention）、temporal super-resolution、运动先验。

### 音频：自回归 + 扩散并存

- **语音合成**：自回归预测 codec token（类似文本生成），或扩散模型在 mel 频谱空间生成
- **音乐生成**：多数用扩散模型，因为音乐的频谱结构更接近"图像"

---

## 4. 跨模态对齐

让不同模态的表示映射到同一向量空间，是多模态理解的基础。

### 对比学习

**CLIP**[^radford-2021-clip]：用大量 (图像, 文本) 对做对比学习——匹配的图文对在向量空间靠近，不匹配的推远。训练后图像和文本共享同一嵌入空间，可以做零样本分类、检索等。

**ImageBind (Meta)**：将 CLIP 思路扩展到六种模态（图像、文本、音频、深度、热成像、IMU），利用图像作为"锚点"桥接所有模态。

### 投影层拼接

早期多模态模型（LLaVA 等）的做法：

```
图像 → 冻结的视觉编码器 (CLIP ViT) → 线性投影 → 拼入 LLM token 序列
```

简单有效，但视觉编码器和 LLM 分别训练，跨模态理解存在 gap。

### 原生多模态训练

Gemini、GPT-4o 的做法：从预训练开始就混合多种模态数据联合训练，模型内部学习对齐。好处是跨模态理解更自然，代价是训练数据工程和算力成本极高。

---

## 5. 开放问题

- **多模态幻觉**：模型"看到"图像中不存在的内容（物体计数错误、空间关系误判）——比纯文本幻觉更难检测
- **评估**：缺乏统一的跨模态评估基准，图像/音频/视频的质量难以用同一把尺子衡量
- **长视频理解**：当前模型对短片段理解不错，但对几分钟以上视频的长程推理仍困难
- **统一生成**：Omni-Model（一个模型同时理解和生成所有模态）仍处早期，跨模态生成质量不均衡

---

## 参考资料

[^dosovitskiy-2020-vit]: Dosovitskiy et al. *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. 2020. https://arxiv.org/abs/2010.11929

[^ho-2020-ddpm]: Ho et al. *Denoising Diffusion Probabilistic Models*. 2020. https://arxiv.org/abs/2006.11239

[^rombach-2022-ldm]: Rombach et al. *High-Resolution Image Synthesis with Latent Diffusion Models*. 2022. https://arxiv.org/abs/2112.10752

[^radford-2021-clip]: Radford et al. *Learning Transferable Visual Models From Natural Language Supervision*. 2021. https://arxiv.org/abs/2103.00020

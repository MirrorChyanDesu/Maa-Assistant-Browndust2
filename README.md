<!-- markdownlint-disable MD033 MD041 -->

<p align="center">
  <img src="mxu_icon.png" width="180" alt="BD2MAA 图标" />
</p>

<div align="center">

# Maa-Assistant-Browndust2

_✨ 《棕色尘埃2》PC 端日常自动化小助手 ✨_

基于 [MaaEnd](https://github.com/MaaEnd/MaaEnd) 改造 · Powered by [MaaFramework](https://github.com/MaaXYZ/MaaFramework) & [MXU](https://github.com/MistEO/MXU)

绝赞开发中 🎉……

</div>

## 📖 使用须知

> ⚠️ **启动方式（重要）**：请通过根目录的 **`launcher.bat`** 启动本软件，**不要直接双击 `mxu.exe`**。
> 首次启动时，launcher 会自动在根目录生成带图标的 **`MaaBd2.lnk`** 快捷方式（指向 launcher.bat）。之后你可以双击这个 lnk，或把它拖到桌面。
> 该启动器会在软件开启时**自动检测 GitHub 新版本**，发现更新时弹出提示窗口，并支持一键下载最新版。
> 更新检测基于 GitHub Releases；选择「一键更新」后会**自动下载并自动覆盖旧版本文件**（`resource/` 等软件文件随版本一并更新），**不会冲掉你的 `config/mxu-MaaBrownDust2.json` 用户配置**——新用户由 MXU 自动生成默认实例；老用户的真实任务实例100% 保留。
> 详细说明见 [更新功能说明](更新功能说明.md)。

- 游戏内语言请使用**简体中文**，并以**窗口化 16:9、1920×1080** 运行（分辨率、方向键等前置设置详见 [注意事项](重要！注意事项！！使用前必看！！！.pdf)）。
- MXU 运行时会在根目录写出一个 0 字节的乱码标记文件（中文“启动”经系统编码后的产物），属上游行为、无害；本项目已自动将其**隐藏并对 git 忽略**

## 📦 项目简介

本项目是基于 [MaaEnd](https://github.com/MaaEnd/MaaEnd) 改造的《棕色尘埃2》PC 端日常自动化工具，运行在 [MaaFramework](https://github.com/MaaXYZ/MaaFramework)（v5.13）运行时之上、由 [MXU](https://github.com/MistEO/MXU)（v2.5）作为 GUI 前端，支持自动日常任务、资源收集、战斗循环等功能。

## ✨ 部分功能说明

- **资源吸收和召集**：自动进入剧情卡带完成“探查 / 吸收 / 召集 / 制伏”，需先按说明配置天赋技能与传送阵（见 [注意事项](重要！注意事项！！使用前必看！！！.pdf)）。
- **分解装备 + 精炼**：一键强化当天“免费抽抽乐”抽出的非 UR 装备后自动分解，并精炼第一页的 18 分装备。
- **启动即检测更新**：打开软件时自动检查 GitHub Releases 新版本，弹窗提示 + 一键下载+自动解压覆盖。覆盖采用"先 .new 再 rename"的原子模式，**中途断电不会留下半截文件**。
- **`debug/` 自动瘦身**：每次启动自动把 MaaFramework 的 `maa.log`（一轮任务 9~16 MB / 2~5 万行）**精简成可读的任务时间线**（约 99% 缩减），原始日志 gzip 归档备查；同时清理超过 7 天的日志、调试截图与归档（可用 `tools\compact_log.ps1` / `tools\clean_logs.ps1` 手动执行，天数见 `updater_config.json` 的 `log_retention_days`）。

## ⚖️ 开源许可证

### 本项目许可证

本项目基于 **AGPL-3.0** 协议开源。

[AGPL-3.0 License](LICENSE)

### 使用的开源项目

本项目使用了以下开源项目（详细致谢、各项目版本与「重新链接」履行说明见 [NOTICE](NOTICE.md)）：

#### 1. MaaXYZ/MaaFramework

- **项目地址**: https://github.com/MaaXYZ/MaaFramework
- **许可证**: **LGPL-3.0**
- **用途**: 运行时核心——图像识别、控制器抽象、任务编排、自定义识别/动作、节点通信
- **使用方式**: 以**动态链接库**形式调用 `maafw/*.dll` / `MaaNode.node`；未修改 MaaFramework 自身源码（LGPL §6「Anti-Distortion」义务最小化）。详见 [NOTICE](NOTICE.md) 第 1 节

#### 2. MistEO/MXU

- **项目地址**: https://github.com/MistEO/MXU
- **许可证**: AGPL-3.0
- **用途**: 桌面 GUI（Tauri）+ Go Agent 子进程 + 实例/设置持久化 + GitHub Releases 检测与下载
- **使用方式**: 单二进制 `mxu.exe`，由 `BD2MAA-Updater.ps1` 自动拉起；与本项目同 AGPL-3.0

#### 3. MaaEnd/MaaEnd

- **项目地址**: https://github.com/MaaEnd/MaaEnd
- **许可证**: AGPL-3.0
- **用途**: 本项目的起点仓库（BD2MAA fork 自 MaaEnd）；保留其工程骨架、目录约定与 AGPL §13 合规继承
- **使用方式**: 继承其任务框架；task-level JSON / pipeline / 图像资源均为本项目重写与扩充

#### 4. PaddlePaddle/PaddleOCR（PP-OCRv5）

- **项目地址**: https://github.com/PaddlePaddle/PaddleOCR
- **许可证**: Apache License 2.0
- **用途**: 游戏内文字识别（OCR）模型
- **使用方式**: 静态模型文件 `resource/model/ocr/{det,rec}.onnx + keys.txt` 随 release zip 派发；由 MaaFramework 的 `OCR` 节点调用推理结果。详见 [NOTICE](NOTICE.md) 第 4 节

## 📜 声明

根据 AGPL-3.0 协议要求：

- 本项目及其衍生项目必须开源
- 任何对本项目的修改必须公开源代码
- 本项目仅供学习交流使用

根据 LGPL-3.0 要求：

- 本项目通过 `maafw/*.dll` 等运行时**动态链接** MaaFramework；运行库自身的源码已在 [MaaXYZ/MaaFramework](https://github.com/MaaXYZ/MaaFramework) 公开
- 用户可通过替换 `maafw/` 目录内的二进制**重新链接**到任意兼容版本的 MaaFramework；步骤见 [NOTICE](NOTICE.md) 「复现/重新链接清单」一节
- 本项目未对 MaaFramework 源码作任何衍生修改，因此 §6 的源码提供义务仅限于原上游

根据 Apache License 2.0 要求：

- 本项目使用了 PaddleOCR 训练的 PP-OCRv5 模型，保留其版权声明于 [NOTICE](NOTICE.md) 第 4 节

## 📥 下载与使用

### 方式一：下载发布版本（推荐）

访问 [Releases](https://github.com/alkaidjin/Maa-Assistant-Browndust2/releases) 页面，下载最新版本的压缩包并解压即可使用。

### 方式二：从源码编译

```bash
# 克隆仓库
git clone https://github.com/alkaidjin/Maa-Assistant-Browndust2.git

# 具体编译步骤请参考 MaaFramework / MXU 官方文档
```

### 自动更新（启动即检测 GitHub 新版本）

本项目的启动器（`launcher.bat` / `BD2MAA-Updater.ps1`）内置 **GitHub Releases 自动更新检测**：

- 每次启动都会先检查仓库是否有新版本；
- 发现新版本会**弹窗提示**（含版本号与更新日志），并可**一键下载**最新压缩包，或前往 GitHub 发布页；
- 检测完成后自动启动 `mxu.exe`；无网络 / 检测失败时也会照常进入软件，不会卡住；
- 选择「一键更新」后会**自动下载、解压并覆盖**旧版本（无需你手动解压合并）；更新时**自动保留 `config/` 下的用户配置**，不会冲掉你自建的任务实例。

### 使用方法

1. **下载/解压后，双击根目录的 `launcher.bat` 启动**（首次启动会自动在根目录生成带图标的 `MaaBd2.lnk`；之后可以双击这个 lnk，或把它拖到桌面）。也可以右键 `launcher.bat` → 发送到桌面快捷方式。
2. 想**预览更新弹窗效果**（即使当前已是最新），用 `launcher.bat -Demo` 运行。
3. 想**强制重新检测**（忽略缓存），用 `launcher.bat -Force` 运行。
4. 仓库地址、检测间隔等可在 `updater_config.json` 中修改。
5. **程序图标**：图标源文件为 `mxu.ico`。MXU 自更新替换 `mxu.exe` 后，`launcher.bat` 下次启动会自动重新写入图标（无需手动操作）。详见 [更新功能说明](更新功能说明.md)。

> 说明：启动器为**纯 PowerShell 实现，零依赖、无需 Python**，详见 [更新功能说明](更新功能说明.md)。

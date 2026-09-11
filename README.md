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

> ⚠️ **启动方式（重要）**：请通过根目录的 **`MaaBd2.lnk`**（已带程序图标的快捷方式，它会调用 `launcher.bat`）启动本软件，**不要直接双击 `mxu.exe`**。
> 该启动器会在软件开启时**自动检测 GitHub 新版本**，发现更新时弹出提示窗口，并支持一键下载最新版。
> 更新检测基于 GitHub Releases；选择「一键更新」后会**自动下载并自动覆盖旧版本文件**（`resource/` 等软件文件随版本一并更新），**仅保留你的 `config/` 用户配置**（如 `mxu-MaaBrownDust2.json`），不会冲掉你自建的任务实例。
> 详细说明见 [更新功能说明](更新功能说明.md)。

- 游戏内语言请使用**简体中文**，并以**窗口化 16:9、1920×1080** 运行（分辨率、方向键等前置设置详见 [注意事项1](注意事项1-----使用前必看！！！.txt)）。
- MXU 运行时会在根目录写出一个 0 字节的乱码标记文件（中文“启动”经系统编码后的产物），属上游行为、无害；本项目已自动将其**隐藏并对 git 忽略**，你不会看到它，也不会被提交进仓库。

## 📦 项目简介

本项目是基于 [MAA](https://github.com/MaaAssistantArknights/MaaAssistantArknights) 框架开发的 BrownDust 游戏自动化工具，支持自动日常任务、资源收集等功能。

## ✨ 部分功能一览

- **资源吸收和召集**：自动进入剧情卡带完成“探查 / 吸收 / 召集 / 制伏”，需先按说明配置天赋技能与传送阵（见 [注意事项1](注意事项1-----使用前必看！！！.txt)）。
- **分解装备 + 精炼**：一键强化当天“免费抽抽乐”抽出的非 UR 装备后自动分解，并精炼第一页的 18 分装备。
- **启动即检测更新**：打开软件时自动检查 GitHub Releases 新版本，弹窗提示 + 一键下载+自动解压覆盖。覆盖采用"先 .new 再 rename"的原子模式，**中途断电不会留下半截文件**。
- **`debug/` 自动瘦身**：每次启动自动把 MaaFramework 的 `maa.log`（一轮任务 9~16 MB / 2~5 万行）**精简成可读的任务时间线**（约 99% 缩减），原始日志 gzip 归档备查；同时清理超过 7 天的日志、调试截图与归档（可用 `tools\compact_log.ps1` / `tools\clean_logs.ps1` 手动执行，天数见 `updater_config.json` 的 `log_retention_days`）。

## ⚖️ 开源许可证

### 本项目许可证

本项目基于 **AGPL-3.0** 协议开源。

[AGPL-3.0 License](LICENSE)

### 使用的开源项目

本项目使用了以下开源项目：

#### 1. MAA (MaaAssistantArknights)

- **项目地址**: https://github.com/MaaAssistantArknights/MaaAssistantArknights
- **许可证**: AGPL-3.0
- **用途**: 游戏自动化框架基础

#### 2. PaddleOCR (PP-OCRv5)

- **项目地址**: https://github.com/PaddlePaddle/PaddleOCR
- **许可证**: Apache License 2.0
- **用途**: 游戏内文字识别（OCR）
- **使用方式**: 调用 PP-OCRv5 移动端文本检测模型

## 📜 声明

根据 AGPL-3.0 协议要求：

- 本项目及其衍生项目必须开源
- 任何对本项目的修改必须公开源代码
- 本项目仅供学习交流使用

根据 Apache License 2.0 要求：

- 本项目使用了 PaddleOCR，保留其版权声明
- 详见 [NOTICE](NOTICE) 文件

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

1. **下载/解压后，双击根目录的 `MaaBd2.lnk`**（已带程序图标的快捷方式）启动；想放桌面就把它拖到桌面即可。也可以右键 `launcher.bat` → 发送到桌面快捷方式。
2. 想**预览更新弹窗效果**（即使当前已是最新），用 `launcher.bat -Demo` 运行。
3. 想**强制重新检测**（忽略缓存），用 `launcher.bat -Force` 运行。
4. 仓库地址、检测间隔等可在 `updater_config.json` 中修改。
5. **程序图标**：图标源文件为 `mxu.ico`。若 MXU 自更新后 `mxu.exe` 图标变回默认，双击 **`应用图标.bat`** 重新应用即可（需先关闭 MXU）。详见 [更新功能说明](更新功能说明.md)。

> 说明：启动器为**纯 PowerShell 实现，零依赖、无需 Python**，详见 [更新功能说明](更新功能说明.md)。

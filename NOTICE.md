# Notice / 第三方致谢

本软件**链接、调用或重新发布**了以下第三方开源项目的代码、模型与运行时。完整许可证文本以仓库根目录的 [LICENSE](LICENSE) 文件为本项目自身条款，以下为各上游条款摘要。

| # | 项目 | 许可证 | 在本项目中的角色 |
|---|---|---|---|
| 1 | [MaaXYZ/MaaFramework](https://github.com/MaaXYZ/MaaFramework)（v5.13.0）| **LGPL-3.0** | 运行时核心（C++ 库 + Node 绑定） |
| 2 | [MistEO/MXU](https://github.com/MistEO/MXU)（v2.5.3） | **AGPL-3.0** | GUI 前端 + Go Agent 子进程 + 实例/设置/自动更新 |
| 3 | [MaaEnd/MaaEnd](https://github.com/MaaEnd/MaaEnd) | **AGPL-3.0** | 本项目起点的「棕色尘埃」适配工程；本仓库 fork 自此 |
| 4 | [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)（PP-OCRv5 移动端）| **Apache-2.0** | OCR 模型（`resource/model/ocr/det.onnx`、`rec.onnx`、`keys.txt`） |

---

## 1. MaaXYZ/MaaFramework — LGPL-3.0

### 用途
提供图像识别、控制器抽象、任务编排、自定义识别/动作注册、节点间通信等核心能力。本项目以**动态链接**的形式使用其预编译二进制作为运行时：

- 静态路由：所有调用均通过 Windows 动态链接库（`.dll` / `.node`）解析，未静态连接，亦未对 MaaFramework 本身的源码进行修改
- 调用入口：见 `resource/pipeline/*.json` 与 `tasks/*.json` 中节点级调用

### 在本项目中的位置
二进制：`maafw/*.dll`、`maafw/MaaNode.node`、`maafw/MaaNodeServer.node`、`maafw/MaaAgent*` |
原始 `LICENSE.md` 文件由 MaaFramework 官方 release zip 一并发布，已随本 release zip 一起派发于 `maafw/`

### LGPL 履约
根据 LGPL-3.0 §6「Anti-Distortion」及 §4「Combined Works」要求：

1. **本项目自身（`BD2MAA`）**采用 **AGPL-3.0**；LGPL 允许与 AGPL 组合发行（AGPL-3.0 §13 / LGPL-3.0 §3「Compatibility with other licenses」）
2. **MaaFramework 库的源码**可在其官方仓库获取（链接见上表），完整 LGPL-3.0 条款文本已随本 release zip 派发在 `maafw/LICENSE.md`
3. **重新链接能力**：如果你想替换或更新 MaaFramework 版本，只需：
   - 关闭 `mxu.exe`
   - 用对应平台、对应主版本号的 `MAA-<platform>-v<version>.zip` 解压并覆盖 `maafw/` 目录（**仅替换 `*.dll/*.node/*.exe`**；保留 `MaaAgentBinary/` 与 `plugins/` 子目录中你不想覆盖的文件）
   - 重新启动 `launcher.bat`
4. **工程加密 / 闭源修改**：本项目对 MaaFramework 库的源码**未做任何修改**，因此 LGPL §6 的「提供源码供用户重新链接」义务不存在

### 版本固定
本仓库当前锁定的 MaaFramework 版本为 `v5.13.0`。如未来升级到新版本，请同步更新本文件上方表格中的版本号，并在 `BD2MAA-Updater.ps1` 的 `MAFW_BASE` 常量、检查 `cache/backup_<version>/` 是否保留旧版本以备回滚。

---

## 2. MistEO/MXU — AGPL-3.0

### 用途
提供桌面 GUI（Tauri / 前端 TypeScript）、设备连接管理、实例配置读写、GitHub Release 检测与下载、`maafw` 子进程（`go-service.exe`）的拉起。

### 在本项目中的位置
单二进制：根目录 `mxu.exe`（v2.5.3）

### AGPL 履约
MXU 与本项目**均为 AGPL-3.0**，因此在 §13 「Remote Network Interaction」的范围内：

1. 本项目以及任何衍生项目若对外提供服务（提供 MXU 前端访问能力），必须同时**完整公开所运行的、与 MXU 相关的全部源代码**，包括任何自定修改
2. MXU 自身的修改若已合并到上游，则「Relicensing」条款不单独适用

### 启动器交互
本项目通过 `BD2MAA-Updater.ps1` / `launcher.bat` **自动拉起** `mxu.exe`，并向其注入 `config/mxu-<project>.json` 中必要的 `savedDevice.windowName` 与 `preAction.waitForExit`（MXU 历史兼容逻辑）。这部分逻辑已经合并到 MXU 上游主分支（v2.5+），本项目侧的注入仅作为兜底保留。

---

## 3. MaaEnd/MaaEnd — AGPL-3.0

### 用途
本仓库为 MaaEnd/MaaEnd 的 fork。最初的任务定义、`interface.json` 框架、`tasks/*.json` 中的 pipeline 编排均来自 MaaEnd 的早期快照。自本仓库创建起，**task-level JSON、resource 下的图像与 OCR pipeline、PaddleOCR 模型副本**均经过大幅改造以适配《棕色尘埃2》特有界面与玩法（如「资源吸收」「召集」「PVP 入口」「EvilCastle 塔」），但**工程骨架与目录约定保留 MaaEnd 原状**。

### AGPL 履约
- 本项目的 AGPL-3.0 许可证与 MaaEnd 同源，**已完成合规继承**：所有 fork 自 MaaEnd 的文件与本项目后续添加的文件统一适用 AGPL-3.0
- MaaEnd 仓库的 commit 历史可通过 `git log --follow <path>` 追溯单个文件的起源

---

## 4. PaddlePaddle/PaddleOCR — Apache-2.0

### 用途
提供 OCR 文本检测与识别模型。PP-OCRv5 移动端模型基于 PaddleOCR 训练并导出，**模型文件以二进制形式跟随本 release zip 派发**：

- `resource/model/ocr/det.onnx`（4.7 MB）
- `resource/model/ocr/rec.onnx`（16.5 MB）
- `resource/model/ocr/keys.txt`（92 KB，字符字典）

### Apache 2.0 履约
1. **版权声明保留**：上述模型来自 PaddleOCR 项目，Apache-2.0 要求「保留版权声明、保留 LICENSE 文件」。模型来自训练产物，已在上方表格列明出处；如需逐文件 LICENSE 副本，可在 PaddleOCR 仓库 `LICENSE` 文件查阅
2. **`NOTICE` 文件**（Notice for PaddleOCR）：如果你在 Apache-2.0 §4(d) 要求的 NOTICE 文件由 PaddleOCR 项目提供，请参阅 [PaddleOCR NOTICE](https://github.com/PaddlePaddle/PaddleOCR/blob/develop/NOTICE)；本项目不创建衍生 NOTICE 文件，只在本文件中汇总
3. **使用方式**：本项目不修改模型权重，仅通过 MaaFramework 的 `MaaOCR` 节点调用推理结果，使用方式见 `resource/pipeline/*.json` 中 type 为 `OCR` 的节点
4. **可重新链接性**：若要换用其他 OCR 模型（如 PaddleOCR 更新版本或其他 OCR 框架），可参考 `tools/make_icon.py` 已有的「下载模型 + 校验 + 替换」流程，将新模型覆盖到 `resource/model/ocr/`，并保持 filenames 一致

---

## 附录：复现 / 重新链接清单

如果你想从源码重建本项目的 `maafw/` / `mxu.exe`：

### MaaFramework（LGPL）
```bash
# 仅当你需要替换 maafw/* 时执行；本项目默认随 release zip 派发预编译版本
curl -L -O https://github.com/MaaXYZ/MaaFramework/releases/download/v5.13.0/MAA-win-x86_64-v5.13.0.zip
# 解压后取 bin/* + share/MaaAgentBinary/*，覆盖到 <BD2MAA>/maafw/
```

### MXU（AGPL）
```bash
git clone https://github.com/MistEO/MXU.git
# 按 MXU 仓库 README 中 AGPL 源的编译说明构建
# 替换 <BD2MAA>/mxu.exe
```

### PaddleOCR（Apache-2.0）
```bash
# 仅当你需要更新 OCR 模型时执行；本项目默认随 release zip 派发
# 从 PaddleOCR 官方仓库拉取对应版本导出 .onnx
# 覆盖 <BD2MAA>/resource/model/ocr/ 下三个文件
```

---

最后更新：2026-09-14

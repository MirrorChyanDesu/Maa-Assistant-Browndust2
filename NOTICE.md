# Notice / 第三方致谢

本软件**链接、调用或重新发布**了以下第三方开源项目的代码、模型与运行时。完整许可证文本以仓库根目录的 [LICENSE](LICENSE) 文件为本项目自身条款，以下为各上游条款摘要。

| # | 项目 | 许可证 | 在本项目中的角色 |
|---|---|---|---|
| 1 | [MaaXYZ/MaaFramework](https://github.com/MaaXYZ/MaaFramework)（v5.13.0）| **LGPL-3.0** | 运行时核心（C++ 库 + Node 绑定） |
| 2 | [MistEO/MXU](https://github.com/MistEO/MXU)（v2.5.3） | **AGPL-3.0** | GUI 前端 + Go Agent 子进程 + 实例/设置/自动更新 |
| 3 | [MaaEnd/MaaEnd](https://github.com/MaaEnd/MaaEnd) | **AGPL-3.0** | 本项目起点的「棕色尘埃」适配工程；本仓库 fork 自此 |
| 4 | [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)（PP-OCRv5 移动端）| **Apache-2.0** | OCR 模型（`resource/model/ocr/det.onnx`、`rec.onnx`、`keys.txt`） |
| 5 | [electron/rcedit](https://github.com/electron/rcedit)（v2.0.0）| **MIT** | 启动器给 `mxu.exe` 写图标的附加工具（`tools/rcedit-x64.exe`） |

---

## 1. MaaXYZ/MaaFramework — LGPL-3.0

### 用途
提供图像识别、控制器抽象、任务编排、自定义识别/动作注册、节点间通信等核心能力。本项目以**动态链接**的形式使用其预编译二进制作为运行时：

- 静态路由：所有调用均通过 Windows 动态链接库（`.dll` / `.node`）解析，未静态连接，亦未对 MaaFramework 本身的源码进行修改
- 调用入口：见 `resource/pipeline/*.json` 与 `tasks/*.json` 中节点级调用

### 本项目中的位置
二进制：`maafw/*.dll`、`maafw/MaaNode.node`、`maafw/MaaNodeServer.node`、`maafw/MaaAgent*`
完整 LGPL-3.0 条款文本随 MaaFramework 官方 release zip 以 `LICENSE.md` 派发；本项目仓库根目录的本文件（`NOTICE.md`）承担**汇总与履约说明**，逐字条款文本可从 [上游 LICENSE.md](https://github.com/MaaXYZ/MaaFramework/blob/main/LICENSE.md) 或官方 release zip 根目录取得。

### LGPL 履约
根据 LGPL-3.0 §6「Anti-Distortion」及 §4「Combined Works」要求：

1. **本项目自身（`BD2MAA`）**采用 **AGPL-3.0**；LGPL 允许与 AGPL 组合发行（AGPL-3.0 §13 / LGPL-3.0 §3「Compatibility with other licenses」）
2. **MaaFramework 库的源码**可在其官方仓库获取（链接见上表）；LGPL-3.0 完整条款文本同样由上游维护，见 [MaaFramework LICENSE.md](https://github.com/MaaXYZ/MaaFramework/blob/main/LICENSE.md)
3. **重新链接能力**：如果你想替换或更新 MaaFramework 版本，只需：
   - 关闭 `mxu.exe`
   - 用对应平台、对应主版本号的 `MAA-<platform>-v<version>.zip` 解压并覆盖 `maafw/` 目录（**仅替换 `*.dll/*.node/*.exe`**；保留 `MaaAgentBinary/` 与 `plugins/` 子目录中你不想覆盖的文件）
   - 重新启动 `launcher.bat`
4. **工程加密 / 闭源修改**：本项目对 MaaFramework 库的源码**未做任何修改**，因此 LGPL §6 的「提供源码供用户重新链接」义务不存在

### 版本固定
本仓库当前锁定的 MaaFramework 版本为 `v5.13.0`。升级到新版本时需要同步维护两处：

1. 本文件上方表格中的版本号（以及 `更新功能说明.md` 第十一节的对照表）；
2. **`version.json`** —— 它记录包内依赖指纹（`maafw` / `mxu` 各自的上游 tag），是打包器 `tools/build_release_zip.py` 在发布计划阶段校验的对象（`check_version_json()` 会提示版本是否与磁盘实际一致，但**不会自动改写**，需要人工确认）。

历史版本备份放在 `cache/backup_<版本>/`（如 `cache/backup_v26.09.6/` 是 v5.7.0-alpha.2 + MXU v1.13.1 的旧运行时）。注意 `cache/` 目录**不随发布包派发**。

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
本项目通过 `launcher.bat` → `BD2MAA-Updater.ps1` **自动拉起** `mxu.exe`：先检查 GitHub Releases 是否有新版本（可一键下载覆盖），再做启动前的「家务」（自愈 `launcher.bat` 编码、按需重写 `mxu.exe` 图标、重建 `MaaBd2.lnk`、精简并清理 `debug/` 日志），最后启动 `mxu.exe`。

**启动器不会修改你的 `config/mxu-<project>.json`。** v26.09.6 曾为绕过 MXU 早期版本的 `savedDevice.windowName` 守卫而注入 `savedDevice.windowName` / `preAction.waitForExit`，该逻辑已在 v26.09.7（随 MXU v2.5.3 升级）**整体移除**——上游守卫改为 `shouldWaitAfterPreActions = !!controller`，不再依赖这两个字段。详见 `更新功能说明.md` 第十、十一节。

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

- `resource/model/ocr/det.onnx`（4.53 MiB）
- `resource/model/ocr/rec.onnx`（15.75 MiB）
- `resource/model/ocr/keys.txt`（92 KiB，字符字典）

### Apache 2.0 履约
1. **版权声明保留**：上述模型来自 PaddleOCR 项目，Apache-2.0 要求「保留版权声明、保留 LICENSE 文件」。模型来自训练产物，已在上方表格列明出处；如需逐文件 LICENSE 副本，可在 PaddleOCR 仓库 `LICENSE` 文件查阅
2. **`NOTICE` 文件**（Notice for PaddleOCR）：如果你在 Apache-2.0 §4(d) 要求的 NOTICE 文件由 PaddleOCR 项目提供，请参阅 [PaddleOCR NOTICE](https://github.com/PaddlePaddle/PaddleOCR/blob/develop/NOTICE)；本项目不创建衍生 NOTICE 文件，只在本文件中汇总
3. **使用方式**：本项目不修改模型权重，仅通过 MaaFramework 的 `MaaOCR` 节点调用推理结果，使用方式见 `resource/pipeline/*.json` 中 type 为 `OCR` 的节点
4. **可替换性**：若要换用其他 OCR 模型（如 PaddleOCR 更新版本或其他 OCR 框架），把新导出的 `det.onnx` / `rec.onnx` / `keys.txt` 覆盖到 `resource/model/ocr/` 即可（保持文件名一致——MaaFramework 的 `OCR` 节点按固定路径加载）。注意这三个文件体积较大、已在 `.gitignore` 中排除，仓库不追踪它们，替换后需要重新打包才会生效。

---

## 5. electron/rcedit — MIT

### 用途
启动器在启动时给 `mxu.exe` 写入图标（`launcher.bat` → `BD2MAA-Updater.ps1` 的 `Apply-ExeIcon`），
使快捷方式与任务栏显示 `mxu.ico`；MXU 自更新替换 `mxu.exe` 后由启动器自动补写，无需用户手动操作。

### 在本项目中的位置
- 二进制：`tools/rcedit-x64.exe`（v2.0.0，GitHub, Inc 官方预编译 x64 构建）
- 随仓库跟踪，并随 release zip 派发；调用点为 `BD2MAA-Updater.ps1` 的 `Apply-ExeIcon`

### MIT 履约
MIT 许可要求保留版权声明与许可声明。本项目以**未经修改**的官方预编译二进制形式再分发，
版权归其原作者所有；上游源码与 `LICENSE` 全文见 [electron/rcedit](https://github.com/electron/rcedit)。

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

最后更新：2026-09-15

# 桌面小工具坑位：PowerShell / WinForms 免安装路线

> 背景：一个四足桌宠实战项目（2026-09-29）。PowerShell + WinForms，无需安装 Python 或任何运行时，双击 bat 启动。83 帧动画：walk 19 / sit 43 / hop 21。

## 坑 1：bat 必须是 CRLF 换行

- **现象**：bat 用 LF 换行时，cmd 会把行劈碎执行，表现为双击闪退、无报错。
- **原因**：cmd 按 CRLF 分行，LF 会被当成行内字符。
- **开工检查项**：
  - [ ] 写完 bat 后跑 `file xxx.bat`，确认输出含 `with CRLF line terminators`。
  - [ ] 在 Linux/VM 上生成 bat 时，换行必须显式写 `\r\n`（如 `printf '...\r\n'` 或 `unix2dos`），不能依赖编辑器默认。
- **最小示例**（启动器模板）：
  ```bat
  @echo off
  rem deskPet launcher - double click to run
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pet.ps1"
  ```
  上面每行行尾都是 CRLF。

## 坑 2：ps1 中文必须 UTF-8 with BOM

- **现象**：ps1 里中文 UI 文案（气泡说话、菜单）在用户机器上显示乱码。
- **原因**：Windows PowerShell 5.1 读无 BOM 的 ps1 时按系统 ANSI 解码，中文直接变乱码。
- **开工检查项**：
  - [ ] 写完 ps1 后检查头 3 字节是 `ef bb bf`（`head -c 3 xxx.ps1 | od -A x -t x1z`）。
  - [ ] 在 Linux 上生成时显式加 BOM：`printf '\xef\xbb\xbf'` 开头，或编辑器保存选 "UTF-8 with BOM"。
  - [ ] 避免在 ps1 里混用全角标点以外的特殊 Unicode 符号，先在实机测一遍显示。

## 坑 3：透明必须用分层窗口逐像素 alpha

- **现象**：用 `TransparencyKey` 做透明，边缘留品红/黑边，动画帧边缘发虚。
- **原因**：TransparencyKey 是整色键抠图，抗锯齿边缘的半透明像素抠不干净。
- **做法**：`SetWindowLong` 加 `WS_EX_LAYERED`，每帧用 `UpdateLayeredWindow` 把带 alpha 通道的位图直接怼上去，逐像素 alpha。
- **开工检查项**：
  - [ ] 代码里出现 `UpdateLayeredWindow` + `WS_EX_LAYERED`，不出现 `TransparencyKey`。
  - [ ] 素材 PNG 自带 alpha 通道（白底 key 透明只在素材生产阶段用，运行时不再抠色）。
  - [ ] 拖动/缩放后边缘无黑边、无描边，肉眼验收一遍。

## 素材管线（动画桌宠）

AI 视频生成（image-to-video，以设定图为参考）→ 按 12fps 抽帧 → 白色背景 key 成透明 → PNG 序列。
抽帧后检查：帧数对得上（walk/sit/跳跃各段别抽混），透明边缘干净。

## 交付检查项

- [ ] bat 是 CRLF，ps1 带 BOM（`file` 双确认）。
- [ ] zip 解压到任意中文路径双击 bat 能跑（路径含空格、含中文都测）。
- [ ] 透明边缘干净，无品红边。
- [ ] 说明.txt 写清：解压→双击 bat→操作方式（拖动/双击/右键）。

## 新坑登记
（以后踩到新坑按"现象→原因→做法→检查项"格式追加到这里）

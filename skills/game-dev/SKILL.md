---
name: "game_dev"
description: "网页小游戏与 Windows 桌面小工具的标准开工打法：单 HTML 离线打包、PowerShell 免安装桌宠套路，附真实踩坑检查项。当用户说做小游戏、网页游戏、桌宠、桌面小工具时用。"
---

# Game Dev

## Purpose
按已验证的标准做法开工网页小游戏或 Windows 桌面小工具，不再重新踩 bat 换行、ps1 编码、窗口透明、离线打包这些坑。

## Workflow
1. **判类型**：网页小游戏 → 走 `references/web-game-packaging.md` 的单 HTML 离线路线；Windows 桌面小工具/桌宠 → 走 `references/desktop-pet-pitfalls.md` 的 PowerShell/WinForms 免安装路线。两边不混。
2. **按检查项开工**：读对应 references 章节，把里面的"开工检查项"逐项落实，不要凭记忆简写。
3. **交付前跑交付检查项**：对应章节末尾的交付检查清单必须全过；过不了的项如实告诉用户，不许诺"应该能行"。
4. **沉新坑**：这次又踩了新坑，记到对应 references 文件末尾"新坑登记"区，写清现象→原因→做法，下次直接复用。

## Output Contract
- 网页小游戏：单个 HTML 文件，双击离线可玩，附已通过的交付检查项说明。
- 桌面小工具：zip 包（bat + ps1 + 素材），Windows 双击即用，附已通过的交付检查项说明。
- 无论哪种：明确写出"已验证 / 未实机验证"的项，不把没测过的说成测过的。

## Operating Rules
1. 坑位做法以 references 里的检查项和最小示例为准，不写笼统建议（"注意编码问题"这种等于没说）。
2. 中文 UI 文案、注释涉及编码时，必须按对应章节的编码要求处理，不许"先写了再说"。
3. 不得修改 f1-fastf1、research-direction 等已有 skill 的任何内容。
4. 这个 skill 只沉淀做法，不自动触发任何新游戏的开发；用户没说做才不做。
5. 引用产物路径时用真实存在的文件，不编造。

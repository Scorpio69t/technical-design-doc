# Technical Design Doc Skill

[![CI](https://github.com/Scorpio69t/technical-design-doc/actions/workflows/ci.yml/badge.svg)](https://github.com/Scorpio69t/technical-design-doc/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Scorpio69t/technical-design-doc)](https://github.com/Scorpio69t/technical-design-doc/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

[English](README.md) | 简体中文

`technical-design-doc` 是一个可移植的 Agent Skill，用于生成、重写和审查面向人类读者的实现级软件详细设计文档。

它把“帮我写一份详细设计”这类宽泛请求，转化为六阶段工程流程：设计边界、架构模型、详细设计、图表设计、人类化改写和质量门禁。

> [下载最新 ZIP 版本](https://github.com/Scorpio69t/technical-design-doc/releases/latest)，也可以按下面的命令直接安装。

## 它解决什么问题

常见的 AI 技术文档问题包括：

- 用一张超大图解释全部系统；
- 正文和图表中的服务、模块名称不一致；
- 时序图只画成功路径，不处理超时、重试和部分失败；
- 已确定的设计与待讨论建议混在一起；
- 正文像 Agent 的执行日志，而不是工程师可评审的设计；
- 只给结论，不解释约束、权衡和边界。

本 Skill 通过固定的工作流解决这些问题，而不是继续堆叠提示词。

## 主要内容

- 包含六阶段工作流的 `SKILL.md`；
- C4 与 Structurizr 模型即代码规范；
- Mermaid 流程图、状态图和 ER 图规范；
- PlantUML 时序图规范与统一样式；
- 去除 AI 腔和 Agent 腔的技术写作规则；
- 详细设计、模块、API、数据库、ADR 和评审模板；
- Structurizr、Mermaid、PlantUML 完整示例；
- 无第三方依赖的文档 linter、Skill 校验器和发布打包器。

## 安装

请选择一种安装位置，并保留整个目录。`references`、`assets` 和 `scripts` 都是 Skill 的组成部分。

### Codex 及兼容客户端

用户级安装：

```bash
git clone https://github.com/Scorpio69t/technical-design-doc.git ~/.agents/skills/technical-design-doc
```

项目级安装（在目标项目根目录执行）：

```bash
git clone https://github.com/Scorpio69t/technical-design-doc.git .agents/skills/technical-design-doc
```

Codex 用户也可以调用 `$skill-installer`，让它从本 GitHub 仓库安装。如果安装后未立即出现，请重启 Codex。

### Claude Code

```bash
git clone https://github.com/Scorpio69t/technical-design-doc.git ~/.claude/skills/technical-design-doc
```

项目级安装请改用 `.claude/skills/technical-design-doc`。

### Cursor

Cursor 可以直接识别上述 `.agents/skills` 路径。也可以使用原生路径：项目级 `.cursor/skills/technical-design-doc`，用户级 `~/.cursor/skills/technical-design-doc`。

### ZIP 安装

从 [GitHub Releases](https://github.com/Scorpio69t/technical-design-doc/releases/latest) 下载带版本号的 ZIP，使用同页的 SHA-256 文件校验后，将顶层 `technical-design-doc` 目录解压到上述任一位置。

## 使用示例

```text
使用 technical-design-doc，基于当前 PRD 和仓库代码生成实现级详细设计。
保留现有服务名称；架构使用 C4，关键写路径使用 PlantUML，状态变化使用
Mermaid；必须包含失败路径、事务、幂等、可观测性，并在交付前执行质量门禁。
```

```text
使用 technical-design-doc 审查这份设计，暂不重写。找出图表过载、边界不清、
失败路径缺失、命名漂移和 AI 腔，并按优先级输出带准确章节引用的评审报告。
```

更多提示词见 [使用配方](references/usage-recipes.md)。

## 本地校验

脚本仅使用 Python 标准库，支持 Python 3.9 及以上版本。

```bash
python scripts/validate_skill.py .
python scripts/lint_design_doc.py examples/sample-detailed-design.md --strict
python -m unittest discover -s tests -v
python scripts/package_skill.py --output-dir dist
```

文档 linter 采用启发式规则，输出是评审提示，不替代架构判断。

## 贡献、安全与许可

提交贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。使用问题请前往 [GitHub Discussions](https://github.com/Scorpio69t/technical-design-doc/discussions)，可复现的问题和改进建议请提交到 [GitHub Issues](https://github.com/Scorpio69t/technical-design-doc/issues)。安全问题不要公开提交 Issue，请遵循 [SECURITY.md](SECURITY.md)。

本项目采用 [MIT License](LICENSE.txt)。

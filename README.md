# PLANS — Priority Logs Actions Notes Stracks

Local-first project management stack system. Built on SQLite with a CLI interface.

## Overview

PLANS provides a local database-driven system for tracking **Plans** (todos),
**Issues**, **Actions**, **Notes**, all organized under **Stracks** (stack/track containers).

Designed for managing local projects that cannot be published to remote repositories.

## Entities

| Entity  | Description                               |
|---------|-------------------------------------------|
| Strack  | Top-level container linking all items     |
| Plan    | Todo item with priority and status        |
| Issue   | Bug/issue with severity tracking          |
| Action  | Actionable task item                      |
| Note    | Free-form documentation note              |

## Installation

```bash
pip install pyplans
```

## Usage

```bash
# Initialize PLANS database
plans <project> init

# ── Strack (container) ──
plans <project> strack create <id> <title> [--description DESC] [--priority N]
plans <project> strack list [--status active|archived]
plans <project> strack show <id>
plans <project> strack delete <id>

# ── Plan (todo) ──
plans <project> plan create <strack_id> <plan_id> <title> [--description DESC] [--priority N]
plans <project> plan list [strack_id] [--status pending|in_progress|done|blocked]
plans <project> plan show <plan_id>
plans <project> plan update <plan_id> --status STATUS
plans <project> plan delete <plan_id>

# ── Issue (bug/task) ──
plans <project> issue create <strack_id> <issue_id> <title> [--description DESC] [--severity SEV]
plans <project> issue list [strack_id] [--status open|in_progress|resolved|closed] [--severity SEV]
plans <project> issue show <issue_id>
plans <project> issue update <issue_id> --status STATUS
plans <project> issue delete <issue_id>

# ── Action (task) ──
plans <project> action create <strack_id> <action_id> <title> [--description DESC]
plans <project> action list [strack_id] [--status pending|in_progress|done|cancelled]
plans <project> action show <action_id>
plans <project> action update <action_id> --status STATUS
plans <project> action delete <action_id>

# ── Note (documentation) ──
plans <project> note create <strack_id> <note_id> <title> [--content CONTENT]
plans <project> note list [strack_id]
plans <project> note show <note_id>
plans <project> note update <note_id> [--title TITLE] [--content CONTENT]
plans <project> note delete <note_id>
```

## License

GPL-3.0-only — See [LICENSE](LICENSE).

---

## 中文文档

PLANS 是一个本地优先（local-first）的项目管理堆栈系统，基于 SQLite 构建，提供命令行界面。

### 概述

PLANS 提供了一套本地数据库驱动的系统，用于跟踪 **Plans**（待办事项）、
**Issues**（问题）、**Actions**（任务）、**Notes**（笔记），
所有条目统一组织在 **Stracks**（堆栈/轨道容器）之下。

专为管理无法发布到远程仓库的本地项目而设计。

### 实体说明

| 实体   | 说明                         |
|--------|------------------------------|
| Strack | 顶层容器，关联所有子条目       |
| Plan   | 待办事项，带优先级和状态       |
| Issue  | 缺陷/问题，带严重程度跟踪      |
| Action | 可执行任务项                  |
| Note   | 自由格式文档笔记              |

### 安装

```bash
pip install pyplans
```

### 使用

```bash
# 初始化 PLANS 数据库
plans <project> init

# ── Strack（容器）──
plans <project> strack create <id> <title> [--description DESC] [--priority N]
plans <project> strack list [--status active|archived]
plans <project> strack show <id>
plans <project> strack delete <id>

# ── Plan（待办事项）──
plans <project> plan create <strack_id> <plan_id> <title> [--description DESC] [--priority N]
plans <project> plan list [strack_id] [--status pending|in_progress|done|blocked]
plans <project> plan show <plan_id>
plans <project> plan update <plan_id> --status STATUS
plans <project> plan delete <plan_id>

# ── Issue（问题/缺陷）──
plans <project> issue create <strack_id> <issue_id> <title> [--description DESC] [--severity SEV]
plans <project> issue list [strack_id] [--status open|in_progress|resolved|closed] [--severity SEV]
plans <project> issue show <issue_id>
plans <project> issue update <issue_id> --status STATUS
plans <project> issue delete <issue_id>

# ── Action（任务）──
plans <project> action create <strack_id> <action_id> <title> [--description DESC]
plans <project> action list [strack_id] [--status pending|in_progress|done|cancelled]
plans <project> action show <action_id>
plans <project> action update <action_id> --status STATUS
plans <project> action delete <action_id>

# ── Note（笔记）──
plans <project> note create <strack_id> <note_id> <title> [--content CONTENT]
plans <project> note list [strack_id]
plans <project> note show <note_id>
plans <project> note update <note_id> [--title TITLE] [--content CONTENT]
plans <project> note delete <note_id>
```

### 许可证

GPL-3.0-only — 详见 [LICENSE](LICENSE)。

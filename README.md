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
pip install .
```

## Usage

```bash
# Initialize PLANS database in current directory
plans init

# Create a new strack
plans strack create my-project "My Project"

# List all stracks
plans strack list

# Create a plan under a strack
plans plan create my-project "Implement login" --priority high

# Create an issue
plans issue create my-project "Login timeout" --severity critical

# List plans in a strack
plans plan list my-project
```

## License

GPL-3.0-only — See [LICENSE](LICENSE).

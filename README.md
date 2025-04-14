# Vaultsync 🚀

A lightweight, zero-dependency Python tool to sync your personal Obsidian vaults.

## What it does

- ✅ Bi-directional sync between **Atlas** (Master vault) and **Orbit** (Work vault)
- ✅ Skips `.obsidian/`, `.git/`, and `/Journals/` folders
- ✅ Appends your **daily work note** from Orbit into your Atlas journal
- ✅ Zero external dependencies — pure Python
- ✅ Manual control: run when you want, no surprises

## Requirements

- Python 3.x
- Unix-like system (tested on Arch Linux)

## Setup

1. Clone the repository
2. Copy `.env.template` to `.env`
3. Set your vault paths in `.env`

Example:
```bash
MASTER_VAULT=/home/youruser/Vaults/atlas
WORK_VAULT=/home/youruser/Vaults/orbit
```

## Usage

Run the sync manually:

```bash
make sync
```

## Notes

- Journals are intentionally excluded from direct sync.
- Work Daily Note is appended into your Atlas journal.
- No dependencies. Fast. Simple. Portable.

## Future Ideas

See TODO.md for future improvements.



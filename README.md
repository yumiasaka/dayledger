# DayLedger

DayLedger is a small, solo-friendly CLI that helps you log daily activities and lightweight expenses into plain-text ledger files. It aims to feel like a personal scratchpad you can grow over time without vendor lock-in.

Why: I wanted a dead-simple way to record what I did and spent each day without spreadsheets or heavy apps. A text-first workflow makes it easy to version, grep, and automate.

## Goals
- Minimal CLI with intuitive commands
- Human-readable storage format (`.day` files)
- Append-only entries with timestamps
- Summaries per day/week/month
- Zero external services

## Roadmap (high level)
- Basic init and add commands
- List and summarize logs
- Tagging and simple filters
- CSV export for expenses
- Optional budgets per tag

## Quick peek
```
dayledger init           # create `.dayledger` folder
dayledger add activity   # log what you did
dayledger add expense    # log an expense
dayledger list           # show entries for today
dayledger sum --month    # quick totals
```

## Non-goals (for now)
- Multi-user sync
- Cloud storage
- Fancy TUI

## License
MIT


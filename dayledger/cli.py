from __future__ import annotations

import argparse
from datetime import datetime, timezone
from .storage import Entry, append_entry, read_entries, ensure_home
from .summary import total_today, by_tag_today


def cmd_init(_: argparse.Namespace) -> int:
  ensure_home()
  print("Initialized .dayledger/")
  return 0


def cmd_add(ns: argparse.Namespace) -> int:
  now = datetime.now(timezone.utc)
  kind = ns.kind
  text = ns.text
  amount = float(ns.amount) if ns.amount is not None else None
  tags = ns.tags.split(",") if ns.tags else None
  entry = Entry(ts=now, kind=kind, text=text, amount=amount, tags=tags)
  path = append_entry(entry)
  print(f"Appended to {path.name}")
  return 0


def cmd_list(_: argparse.Namespace) -> int:
  entries = read_entries()
  for e in entries:
    amount = f" | {e.amount:.2f}" if e.amount is not None else ""
    tags = f" | #{','.join(e.tags)}" if e.tags else ""
    print(f"{e.ts.isoformat()} | {e.kind} | {e.text}{amount}{tags}")
  return 0


def build_parser() -> argparse.ArgumentParser:
  p = argparse.ArgumentParser(prog="dayledger", description="Log daily activities and expenses")
  sub = p.add_subparsers(dest="cmd", required=True)

  sp = sub.add_parser("init", help="create storage folder")
  sp.set_defaults(func=cmd_init)

  sp = sub.add_parser("add", help="add an entry")
  sp.add_argument("kind", choices=["activity", "expense"], help="type of entry")
  sp.add_argument("text", help="description text")
  sp.add_argument("--amount", help="amount for expense", required=False)
  sp.add_argument("--tags", help="comma-separated tags", required=False)
  sp.set_defaults(func=cmd_add)

  sp = sub.add_parser("list", help="list today entries")
  sp.set_defaults(func=cmd_list)

  sp = sub.add_parser("sum", help="show today totals")
  def _sum(_: argparse.Namespace) -> int:
    print(f"total: {total_today():.2f}")
    for k, v in by_tag_today().items():
      print(f"{k}: {v:.2f}")
    return 0
  sp.set_defaults(func=_sum)

  return p


def main(argv: list[str] | None = None) -> int:
  parser = build_parser()
  ns = parser.parse_args(argv)
  return ns.func(ns)


if __name__ == "__main__":
  raise SystemExit(main())

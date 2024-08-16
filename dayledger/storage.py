from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DIR = Path.cwd() / ".dayledger"


def ensure_home(dir_path: Path = DEFAULT_DIR) -> Path:
  dir_path.mkdir(parents=True, exist_ok=True)
  return dir_path


def today_filename(ts: datetime | None = None) -> str:
  when = ts or datetime.now(timezone.utc)
  return when.strftime("%Y-%m-%d.day")


def file_for(ts: datetime | None = None, dir_path: Path = DEFAULT_DIR) -> Path:
  return ensure_home(dir_path) / today_filename(ts)


@dataclass
class Entry:
  ts: datetime
  kind: str  # "activity" or "expense"
  text: str
  amount: float | None = None
  tags: list[str] | None = None

  def to_line(self) -> str:
    t = self.ts.astimezone(timezone.utc).isoformat()
    parts = [t, self.kind, self.text]
    if self.amount is not None:
      parts.append(f"{self.amount:.2f}")
    if self.tags:
      parts.append("#" + ",".join(self.tags))
    return " | ".join(parts)


def append_entry(entry: Entry, dir_path: Path = DEFAULT_DIR) -> Path:
  path = file_for(entry.ts, dir_path)
  with path.open("a", encoding="utf-8") as f:
    f.write(entry.to_line() + "\n")
  return path


def read_entries(ts: datetime | None = None, dir_path: Path = DEFAULT_DIR) -> list[Entry]:
  path = file_for(ts, dir_path)
  if not path.exists():
    return []
  entries: list[Entry] = []
  with path.open("r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if not line:
        continue
      parts = [p.strip() for p in line.split("|")]
      try:
        ts = datetime.fromisoformat(parts[0])
        kind = parts[1]
        text = parts[2]
        amount = None
        tags: list[str] | None = None
        if len(parts) >= 4 and parts[3]:
          try:
            amount = float(parts[3])
          except ValueError:
            amount = None
        if len(parts) >= 5 and parts[4].startswith("#"):
          tags = parts[4][1:].split(",") if parts[4][1:] else []
        entries.append(Entry(ts=ts, kind=kind, text=text, amount=amount, tags=tags))
      except Exception:
        continue
  return entries


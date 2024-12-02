from __future__ import annotations

from collections import defaultdict
from .storage import read_entries


def total_today() -> float:
  total = 0.0
  for e in read_entries():
    if e.amount is not None:
      total += e.amount
  return round(total, 2)


def by_tag_today() -> dict[str, float]:
  agg: dict[str, float] = defaultdict(float)
  for e in read_entries():
    if e.amount is not None and e.tags:
      for t in e.tags:
        agg[t] += e.amount
  return {k: round(v, 2) for k, v in agg.items()}


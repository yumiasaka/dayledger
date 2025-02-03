from dayledger.storage import Entry, append_entry, read_entries
from datetime import datetime, timezone
from pathlib import Path

def test_append_and_read(tmp_path: Path):
    when = datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    e = Entry(ts=when, kind="expense", text="tea", amount=2.5, tags=["drink"])
    d = tmp_path / ".dayledger"
    append_entry(e, dir_path=d)
    items = read_entries(ts=when, dir_path=d)
    assert len(items) == 1
    assert items[0].text == "tea"

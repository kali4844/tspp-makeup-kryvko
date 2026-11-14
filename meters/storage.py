"""Шар даних: єдине місце, що знає, де і як зберігаються записи."""
import json
import os


def _path():
    return os.environ.get("METERS_DATA", "data.json")


def load():
    """Усі записи у порядку збереження."""
    if not os.path.exists(_path()):
        return []
    with open(_path(), encoding="utf-8") as f:
        return json.load(f)


def save(records):
    """Повністю замінити записи переданими."""
    with open(_path(), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

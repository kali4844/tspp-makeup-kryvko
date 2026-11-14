"""Показники лічильників: додавання і споживання за місяць."""
import json
import os
from datetime import datetime


def data_path():
    return os.environ.get("METERS_DATA", "data.json")


def add(counter, value, date):
    if value < 0:
        raise ValueError("значення показника не може бути від'ємним")
    records = []
    if os.path.exists(data_path()):
        with open(data_path(), encoding="utf-8") as f:
            records = json.load(f)
    records.append({"counter": counter, "value": value, "date": date})
    with open(data_path(), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def consumption(counter, month):
    """Споживання лічильника за місяць 'YYYY-MM'."""
    datetime.strptime(month, "%Y-%m")
    if not os.path.exists(data_path()):
        return 0
    with open(data_path(), encoding="utf-8") as f:
        records = json.load(f)
    mine = [r for r in records if r["counter"] == counter]
    in_month = [r for r in mine if r["date"].startswith(month)]
    before = [r for r in mine if r["date"] < month + "-01"]
    if not in_month:
        return 0
    base = before[-1]["value"] if before else in_month[0]["value"]
    return in_month[-1]["value"] - base

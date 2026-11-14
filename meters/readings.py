"""Показники лічильників: додавання і споживання за місяць."""
from datetime import datetime

from meters import storage


def add(counter, value, date):
    if value < 0:
        raise ValueError("значення показника не може бути від'ємним")
    records = storage.load()
    records.append({"counter": counter, "value": value, "date": date})
    storage.save(records)


def consumption(counter, month):
    """Споживання лічильника за місяць 'YYYY-MM'."""
    datetime.strptime(month, "%Y-%m")
    mine = [r for r in storage.load() if r["counter"] == counter]
    in_month = [r for r in mine if r["date"].startswith(month)]
    before = [r for r in mine if r["date"] < month + "-01"]
    if not in_month:
        return 0
    base = before[-1]["value"] if before else in_month[0]["value"]
    return in_month[-1]["value"] - base

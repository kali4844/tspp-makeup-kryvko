"""Рахунок за місяць і пошук підозрілих показників."""
import json
import os
from datetime import datetime

from meters import readings

MAX_JUMP = 500  # найбільший звичайний приріст між двома показниками
DECREASE = "значення менше попереднього"
JUMP = "різкий стрибок"


def _load():
    if not os.path.exists(readings.data_path()):
        return []
    with open(readings.data_path(), encoding="utf-8") as f:
        return json.load(f)


def bill(month, tariff):
    """Сума до сплати за місяць: споживання всіх лічильників × тариф за одиницю."""
    datetime.strptime(month, "%Y-%m")
    counters = {r["counter"] for r in _load()}
    total = sum(readings.consumption(c, month) for c in sorted(counters))
    return round(total * tariff, 2)


def _reason(previous, value):
    """Чому показник підозрілий, або None, якщо все гаразд."""
    if value < previous:
        return DECREASE
    if value - previous > MAX_JUMP:
        return JUMP
    return None


def anomalies():
    """Підозрілі показники: значення менше за попереднє або стрибок понад MAX_JUMP."""
    result = []
    last = {}
    for r in _load():
        counter = r["counter"]
        if counter in last:
            reason = _reason(last[counter], r["value"])
            if reason:
                result.append((counter, r["date"], reason))
        last[counter] = r["value"]
    return result

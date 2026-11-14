"""Рахунок за місяць і пошук підозрілих показників."""
import json
import os
from datetime import datetime

from meters import readings


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


def anomalies():
    """Підозрілі показники: значення менше за попереднє або стрибок понад 500."""
    result = []
    last = {}
    for r in _load():
        counter = r["counter"]
        if counter in last:
            if r["value"] < last[counter]:
                result.append((counter, r["date"], "значення менше попереднього"))
            else:
                if r["value"] - last[counter] > 500:
                    result.append((counter, r["date"], "різкий стрибок"))
        last[counter] = r["value"]
    return result

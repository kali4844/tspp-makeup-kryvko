"""Рахунок за місяць і пошук підозрілих показників."""
from datetime import datetime

from meters import readings, storage

MAX_JUMP = 500  # найбільший звичайний приріст між двома показниками
DECREASE = "значення менше попереднього"
JUMP = "різкий стрибок"


def bill(month, tariff):
    """Сума до сплати за місяць: споживання всіх лічильників × тариф за одиницю."""
    datetime.strptime(month, "%Y-%m")
    counters = {r["counter"] for r in storage.load()}
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
    for r in storage.load():
        counter = r["counter"]
        if counter in last:
            reason = _reason(last[counter], r["value"])
            if reason:
                result.append((counter, r["date"], reason))
        last[counter] = r["value"]
    return result


def top_consumers(month, n):
    """Повертає n лічильників з найбільшим споживанням; рівні — за назвою лічильника."""
    counters = sorted({r["counter"] for r in storage.load()})
    totals = {c: readings.consumption(c, month) for c in counters}
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]

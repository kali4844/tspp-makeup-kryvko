# Розбір коду від ШІ: `billing.top_consumers`

## Промпт (дослівно)

> У мене є консольний Python-проєкт «Облік показників лічильників» (пакет `meters`, модулі `readings`, `billing`, `storage`).
> Напиши в `meters/billing.py` функцію `top_consumers(month, n)`, яка повертає `n` лічильників з найбільшим споживанням
> за місяць у форматі `YYYY-MM`. Додай тести pytest.

## Відповідь ШІ (дослівно)

Додайте в `meters/billing.py`:

```python
def top_consumers(month, n):
    """Повертає n лічильників з найбільшим споживанням за місяць."""
    counters = {r["counter"] for r in storage.load()}
    totals = {c: readings.consumption(c, month) for c in counters}
    return sorted(totals.items(), key=lambda item: item[1], reverse=True)[:n]
```

І тести в `tests/test_top_consumers.py`:

```python
import pytest

from meters import billing, readings


@pytest.fixture(autouse=True)
def data_file(tmp_path, monkeypatch):
    monkeypatch.setenv("METERS_DATA", str(tmp_path / "data.json"))


def test_top_consumers_returns_largest_first():
    for counter, date, value in [
        ("a", "2026-09-30", 0), ("a", "2026-10-31", 10),
        ("b", "2026-09-30", 0), ("b", "2026-10-31", 40),
        ("c", "2026-09-30", 0), ("c", "2026-10-31", 25),
    ]:
        readings.add(counter, value, date)
    assert billing.top_consumers("2026-10", 2) == [("b", 40), ("c", 25)]


def test_top_consumers_returns_list():
    readings.add("a", 5, "2026-10-01")
    assert isinstance(billing.top_consumers("2026-10", 1), list)
```

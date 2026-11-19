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


def test_equal_consumption_is_ordered_by_counter_name():
    for counter in "hgfedcba":
        readings.add(counter, 0, "2026-09-30")
        readings.add(counter, 10, "2026-10-31")
    result = billing.top_consumers("2026-10", 8)
    assert [name for name, _ in result] == list("abcdefgh")

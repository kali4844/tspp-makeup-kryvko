import pytest

from meters import readings


@pytest.fixture(autouse=True)
def data_file(tmp_path, monkeypatch):
    monkeypatch.setenv("METERS_DATA", str(tmp_path / "data.json"))


def fill(*rows):
    for date, value in rows:
        readings.add("m1", value, date)


def test_single_reading_in_month_gives_zero():  # R1, межа
    fill(("2026-10-15", 100))
    assert readings.consumption("m1", "2026-10") == 0


def test_two_readings_in_month_give_last_minus_first():  # R2
    fill(("2026-10-05", 100), ("2026-10-25", 130))
    assert readings.consumption("m1", "2026-10") == 30


def test_base_is_last_reading_of_previous_month():  # R3, межа
    fill(("2026-09-30", 100), ("2026-10-10", 120))
    assert readings.consumption("m1", "2026-10") == 20


def test_first_day_of_next_month_is_not_counted():  # R4, межа
    fill(("2026-09-30", 100), ("2026-10-31", 140), ("2026-11-01", 150))
    assert readings.consumption("m1", "2026-10") == 40


def test_nonexistent_month_raises_value_error():  # R5, недійсний вхід
    with pytest.raises(ValueError):
        readings.consumption("m1", "2026-13")

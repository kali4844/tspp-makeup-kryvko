import pytest

from meters import billing, readings


@pytest.fixture(autouse=True)
def data_file(tmp_path, monkeypatch):
    monkeypatch.setenv("METERS_DATA", str(tmp_path / "data.json"))


def test_bill_is_total_consumption_times_tariff():
    for counter, date, value in [
        ("m1", "2026-09-30", 100),
        ("m1", "2026-10-31", 140),
        ("m2", "2026-09-30", 10),
        ("m2", "2026-10-31", 20),
    ]:
        readings.add(counter, value, date)
    assert billing.bill("2026-10", 2.5) == 125.0


def test_anomalies_reports_decrease_and_jump():
    for counter, date, value in [
        ("m1", "2026-09-01", 100),
        ("m1", "2026-09-02", 90),
        ("m1", "2026-09-03", 700),
        ("m2", "2026-09-01", 5),
        ("m2", "2026-09-02", 10),
    ]:
        readings.add(counter, value, date)
    assert billing.anomalies() == [
        ("m1", "2026-09-02", "значення менше попереднього"),
        ("m1", "2026-09-03", "різкий стрибок"),
    ]

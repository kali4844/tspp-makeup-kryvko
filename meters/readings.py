"""Показники лічильників: додавання і споживання за місяць."""
import logging
from datetime import datetime

from meters import storage

logger = logging.getLogger(__name__)


def add(counter, value, date):
    logger.info("add: counter=%s date=%s", counter, date)
    if value < 0:
        logger.error("add rejected: counter=%s date=%s reason=negative value", counter, date)
        raise ValueError("значення показника не може бути від'ємним")
    records = storage.load()
    records.append({"counter": counter, "value": value, "date": date})
    storage.save(records)


def _check_month(counter, month):
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        logger.error(
            "consumption rejected: counter=%s month=%r reason=month is not YYYY-MM", counter, month
        )
        raise


def consumption(counter, month):
    """Споживання лічильника за місяць 'YYYY-MM'."""
    logger.info("consumption: counter=%s month=%s", counter, month)
    _check_month(counter, month)
    mine = [r for r in storage.load() if r["counter"] == counter]
    in_month = [r for r in mine if r["date"].startswith(month)]
    before = [r for r in mine if r["date"] < month + "-01"]
    if not in_month:
        return 0
    base = before[-1] if before else in_month[0]
    last = in_month[-1]
    result = last["value"] - base["value"]
    logger.info(
        "consumption result: counter=%s month=%s base_date=%s last_date=%s result=%s",
        counter, month, base["date"], last["date"], result,
    )
    return result

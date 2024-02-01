from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo
import math


def is_last_weekday_of_the_month(on_date: date, weekday: int) -> bool:
    """
    Check if a given date is the last weekday of the month

    Args:
        on_date: datetime.date
        weekday: int (0: Mon, 1: Tue, ..., 6: Sun)

    Returns:
        True if on_date is last weekday of the month, False otherwise
    """
    return (
        on_date.weekday() == weekday
        and (on_date + timedelta(days=7)).month != on_date.month
    )


def is_last_thursday_of_the_month(on_date: date) -> bool:
    """
    Check if a given date is the last Thursday of the month

    Args:
        on_date: datetime.date

    Returns:
        True if on_date is last Thursday of the month, False otherwise
    """
    return is_last_weekday_of_the_month(on_date=on_date, weekday=3)


def is_last_wednesday_of_the_month(on_date: date) -> bool:
    """
    Check if a given date is the last Wednesday of the month

    Args:
        on_date: datetime.date

    Returns:
        True if on_date is last Wednesday of the month, False otherwise
    """
    return is_last_weekday_of_the_month(on_date=on_date, weekday=2)


def get_cache_expiry_seconds(
    now: datetime, tz: ZoneInfo = ZoneInfo(key="Asia/Calcutta")
) -> int:
    """
    Get secs from now till end of day

    Args:
        now: datetime

    Returns:
        int
    """
    next_day: datetime = now + timedelta(days=1)
    next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)

    return math.ceil((next_day - now).total_seconds())

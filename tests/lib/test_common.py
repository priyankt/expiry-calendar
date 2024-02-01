from datetime import date, datetime
from zoneinfo import ZoneInfo
import pytest

from src.lib.common import is_last_thursday_of_the_month, get_cache_expiry_seconds


@pytest.mark.parametrize(
    "test_date, expected_result",
    [
        (date(year=2024, month=1, day=25), True),
        (date(year=2024, month=1, day=18), False),
        (date(year=2024, month=1, day=17), False),
        (date(year=2024, month=2, day=29), True),
    ],
)
def test_is_last_thursday_of_the_month(test_date: date, expected_result: bool) -> None:
    assert is_last_thursday_of_the_month(on_date=test_date) == expected_result


@pytest.mark.parametrize(
    "test_now, secs",
    [
        (
            datetime(
                year=2024,
                month=1,
                day=25,
                hour=23,
                tzinfo=ZoneInfo(key="Asia/Calcutta"),
            ),
            3600,
        ),
        (datetime(year=2024, month=1, day=25, hour=15), 3600 * 9),
        (datetime(year=2024, month=1, day=25, hour=1), 3600 * 23),
        (datetime(year=2024, month=1, day=25, hour=8), 3600 * 16),
        (datetime(year=2024, month=1, day=25, hour=23, minute=30), 1800),
        (datetime(year=2024, month=1, day=25, hour=23, minute=59), 60),
        (datetime(year=2024, month=1, day=25, hour=23, minute=59, second=59), 1),
        (datetime(year=2024, month=1, day=25, hour=20, minute=55), (3 * 3600) + 300),
    ],
)
def test_get_cache_expiry_seconds(test_now: datetime, secs: int) -> None:
    assert get_cache_expiry_seconds(now=test_now) == secs

from datetime import date
import pytest

from src.lib.common import is_last_thursday_of_the_month


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

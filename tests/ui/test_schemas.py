from typing import List
from datetime import date
import pytest

from src.domain.schemas import Instrument
from src.ui.schemas import ExpirySection


@pytest.mark.parametrize(
    "test_instrument, expected_result",
    [
        (Instrument(name="NIFTY", lot_size=50, expiry_dow=3), True),
        (Instrument(name="SENSEX", lot_size=10, expiry_dow=4), True),
        (Instrument(name="BANKNIFTY", lot_size=15, expiry_dow=3), True),
    ],
)
def test_is_monthly_expiry(test_instrument: Instrument, expected_result: bool) -> None:
    expiry_section = ExpirySection(
        date=date(year=2024, month=1, day=25), instruments=[], is_selected=False
    )
    assert (
        expiry_section.is_monthly_expiry(for_instrument=test_instrument)
        == expected_result
    )

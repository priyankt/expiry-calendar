from typing import List
from datetime import date
import pytest

from src.domain.schemas import Exchange, Holiday, Instrument, Market

midcpnifty: Instrument = Instrument(name="MIDCPNIFTY", lot_size=75, expiry_dow=0)
finnifty: Instrument = Instrument(name="FINNIFTY", lot_size=75, expiry_dow=1)
banknifty: Instrument = Instrument(name="BANKNIFTY", lot_size=15, expiry_dow=2)
nifty: Instrument = Instrument(name="NIFTY", lot_size=50, expiry_dow=3)
bankex: Instrument = Instrument(name="BANKEX", lot_size=15, expiry_dow=0)
sensex: Instrument = Instrument(name="SENSEX", lot_size=10, expiry_dow=4)

holidays: List[Holiday] = [
    Holiday(date=date(year=2024, month=1, day=26), description="Republic Day"),
    Holiday(date=date(year=2024, month=3, day=8), description="Mahashivratri"),
    Holiday(date=date(year=2024, month=3, day=25), description="Holi"),
]
nse: Exchange = Exchange(
    name="NSE", holidays=holidays, instruments=[midcpnifty, finnifty, banknifty, nifty]
)
bse: Exchange = Exchange(name="BSE", holidays=holidays, instruments=[bankex, sensex])
market: Market = Market(exchanges=[nse, bse])


@pytest.mark.parametrize(
    "test_date, expected_result",
    [
        (date(year=2024, month=1, day=26), True),
        (date(year=2024, month=1, day=29), False),
    ],
)
def test_exchange_is_holiday(test_date: date, expected_result: bool) -> None:
    assert nse.is_holiday(on_date=test_date) == expected_result


@pytest.mark.parametrize(
    "test_date, expected_business_date",
    [
        (date(year=2024, month=1, day=25), date(year=2024, month=1, day=26)),
        (date(year=2024, month=1, day=26), date(year=2024, month=1, day=29)),
        (date(year=2024, month=1, day=22), date(year=2024, month=1, day=23)),
    ],
)
def test_next_business_date(test_date: date, expected_business_date: date) -> None:
    assert nse.next_business_date(after_date=test_date) == expected_business_date


@pytest.mark.parametrize(
    "test_date, expected_trading_date",
    [
        (date(year=2024, month=1, day=25), date(year=2024, month=1, day=29)),
        (date(year=2024, month=1, day=19), date(year=2024, month=1, day=22)),
        (date(year=2024, month=1, day=18), date(year=2024, month=1, day=19)),
    ],
)
def test_next_trading_date(test_date: date, expected_trading_date: date) -> None:
    assert nse.next_trading_date(after_date=test_date) == expected_trading_date


@pytest.mark.parametrize(
    "test_date, expected_expiring_instruments",
    [
        (date(year=2024, month=1, day=25), [sensex]),
        (date(year=2024, month=1, day=27), []),
        (date(year=2024, month=1, day=29), [bankex]),
        (date(year=2024, month=1, day=30), []),
        (date(year=2024, month=1, day=31), []),
    ],
)
def test_bse_expiring_instruments(
    test_date: date, expected_expiring_instruments: List[Instrument]
) -> None:
    print(f"{test_date}, {expected_expiring_instruments}")
    assert bse.expiring_instruments(on_date=test_date) == expected_expiring_instruments


@pytest.mark.parametrize(
    "test_date, expected_expiring_instruments",
    [
        (date(year=2024, month=1, day=25), [nifty, banknifty]),
        (date(year=2024, month=1, day=27), []),
        (date(year=2024, month=1, day=29), [midcpnifty]),
        (date(year=2024, month=1, day=30), [finnifty]),
        (date(year=2024, month=1, day=31), [banknifty]),
    ],
)
def test_nse_expiring_instruments(
    test_date: date, expected_expiring_instruments: List[Instrument]
) -> None:
    assert sorted(nse.expiring_instruments(on_date=test_date)) == sorted(
        expected_expiring_instruments
    )


@pytest.mark.parametrize(
    "test_date, expected_expiring_instruments",
    [
        (date(year=2024, month=1, day=25), [nifty, sensex, banknifty]),
        (date(year=2024, month=1, day=27), []),
        (date(year=2024, month=1, day=29), [midcpnifty, bankex]),
        (date(year=2024, month=1, day=30), [finnifty]),
        (date(year=2024, month=1, day=31), [banknifty]),
        (date(year=2024, month=3, day=7), [nifty, sensex]),
        (date(year=2024, month=3, day=22), [midcpnifty, sensex, bankex]),
        (date(year=2024, month=3, day=23), []),
        (date(year=2024, month=3, day=24), []),
    ],
)
def test_market_expiring_instruments(
    test_date: date, expected_expiring_instruments: List[Instrument]
) -> None:
    assert sorted(market.expiring_instruments(on_date=test_date)) == sorted(
        expected_expiring_instruments
    )


@pytest.mark.parametrize(
    "instrument, expected_result",
    [(banknifty, True), (bankex, False), (finnifty, False)],
)
def test_instrument_is_banknifty(instrument: Instrument, expected_result: bool) -> None:
    assert instrument.is_banknifty() == expected_result


@pytest.mark.parametrize(
    "date, expected_result",
    [
        (date(year=2024, month=1, day=25), True),
        (date(year=2024, month=1, day=17), True),
        (date(year=2024, month=1, day=3), True),
        (date(year=2024, month=1, day=31), True),
        (date(year=2024, month=1, day=4), False),
        (date(year=2024, month=1, day=24), False),
    ],
)
def test_is_banknifty_expiring(date: date, expected_result: bool) -> None:
    assert banknifty.is_banknifty_expiring(on_date=date) == expected_result

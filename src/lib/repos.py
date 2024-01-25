from typing import List
from datetime import date

from src.domain.schemas import Holiday, Market, Exchange, Instrument


def fetch_holidays() -> List[Holiday]:
    """
    Returns holidays

    Args:
        none

    Returns:
        List of Holiday objects
    """
    return [
        Holiday(date=date(year=2024, month=1, day=22), description="Special Holiday"),
        Holiday(date=date(year=2024, month=1, day=26), description="Republic Day"),
        Holiday(date=date(year=2024, month=3, day=8), description="Mahashivratri"),
        Holiday(date=date(year=2024, month=3, day=25), description="Holi"),
        Holiday(date=date(year=2024, month=3, day=29), description="Good Friday"),
        Holiday(
            date=date(year=2024, month=4, day=11),
            description="Id-Ul-Fitr (Ramadan Eid)",
        ),
        Holiday(
            date=date(year=2024, month=4, day=14),
            description="Dr. Baba Saheb Ambedkar Jayanti",
        ),
        Holiday(date=date(year=2024, month=4, day=17), description="Shri Ram Navmi"),
        Holiday(
            date=date(year=2024, month=4, day=21), description="Shri Mahavir Jayanti"
        ),
        Holiday(date=date(year=2024, month=5, day=1), description="Maharashtra Day"),
        Holiday(date=date(year=2024, month=6, day=17), description="Bakri Id"),
        Holiday(date=date(year=2024, month=7, day=17), description="Moharram"),
        Holiday(date=date(year=2024, month=8, day=15), description="Independence Day"),
        Holiday(date=date(year=2024, month=9, day=7), description="Ganesh Chaturthi"),
        Holiday(
            date=date(year=2024, month=10, day=2), description="Mahatma Gandhi Jayanti"
        ),
        Holiday(date=date(year=2024, month=10, day=12), description="Dussehra"),
        Holiday(
            date=date(year=2024, month=11, day=1), description="Diwali Laxmi Pujan"
        ),
        Holiday(
            date=date(year=2024, month=11, day=2), description="Diwali-Balipratipada"
        ),
        Holiday(
            date=date(year=2024, month=11, day=15), description="Gurunanak Jayanti"
        ),
        Holiday(date=date(year=2024, month=12, day=25), description="Christmas"),
    ]


def get_nse() -> Exchange:
    """
    Returns NSE exchange object

    Args:
        none

    Returns:
        Exchange object
    """
    return Exchange(
        name="NSE",
        holidays=fetch_holidays(),
        instruments=[
            Instrument(name="MIDCPNIFTY", lot_size=75, expiry_dow=0),
            Instrument(name="FINNIFTY", lot_size=40, expiry_dow=1),
            Instrument(name="BANKNIFTY", lot_size=15, expiry_dow=2),
            Instrument(name="NIFTY", lot_size=50, expiry_dow=3),
        ],
    )


def get_bse() -> Exchange:
    """
    Returns BSE exchange object

    Args:
        none

    Returns:
        Exchange object
    """
    return Exchange(
        name="BSE",
        holidays=fetch_holidays(),
        instruments=[
            Instrument(name="BANKEX", lot_size=15, expiry_dow=0),
            Instrument(name="SENSEX", lot_size=10, expiry_dow=4),
        ],
    )


def get_market() -> Market:
    """
    Returns Market with multiple exchanges

    Args:
        none

    Returns:
        Market Object
    """
    return Market(exchanges=[get_nse(), get_bse()])

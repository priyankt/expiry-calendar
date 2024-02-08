from typing import List, cast
from datetime import date

from sqlalchemy.orm import Session
from src.lib.models import Holiday as DBHoliday
from src.lib.common import get_today

from src.domain.schemas import Holiday, Market, Exchange, Instrument


def fetch_holidays(db: Session, current_date: date = get_today()) -> List[Holiday]:
    """
    Returns holidays from database

    Args:
        db: Session
        current_date: date (default: get_today())

    Returns:
        List of Holiday objects
    """
    holidays: List[DBHoliday] = (
        db.query(DBHoliday).filter(DBHoliday.date >= current_date).all()
    )
    return list(
        map(
            lambda x: Holiday(
                date=cast(date, x.date),
                description=cast(str, x.title),
            ),
            holidays,
        )
    )


def get_nse(db: Session) -> Exchange:
    """
    Returns NSE exchange object

    Args:
        none

    Returns:
        Exchange object
    """
    return Exchange(
        name="NSE",
        holidays=fetch_holidays(db=db),
        instruments=[
            Instrument(name="MIDCPNIFTY", lot_size=75, expiry_dow=0),
            Instrument(name="FINNIFTY", lot_size=40, expiry_dow=1),
            Instrument(name="BANKNIFTY", lot_size=15, expiry_dow=2),
            Instrument(name="NIFTY", lot_size=50, expiry_dow=3),
        ],
    )


def get_bse(db: Session) -> Exchange:
    """
    Returns BSE exchange object

    Args:
        none

    Returns:
        Exchange object
    """
    return Exchange(
        name="BSE",
        holidays=fetch_holidays(db=db),
        instruments=[
            Instrument(name="BANKEX", lot_size=15, expiry_dow=0),
            Instrument(name="SENSEX", lot_size=10, expiry_dow=4),
        ],
    )


def get_market(db: Session) -> Market:
    """
    Returns Market with multiple exchanges

    Args:
        none

    Returns:
        Market Object
    """
    return Market(exchanges=[get_nse(db), get_bse(db)])

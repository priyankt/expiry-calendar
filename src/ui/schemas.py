from typing import List
from datetime import date
from pydantic import BaseModel

from src.domain.schemas import Instrument
from src.lib.common import is_last_weekday_of_the_month


class ExpirySection(BaseModel):
    date: date
    instruments: List[Instrument]
    is_selected: bool = False

    def is_monthly_expiry(self, for_instrument: Instrument) -> bool:
        """
        Check if its a monthly expiry for given instrument. It expects the instruments
        variable to be properly populated.

        Args:
            for_instrument: Instrument

        Returns:
            True if for_instrument has monthly expiry on date else False
        """
        dow: int = self.date.weekday()
        # Bank Nifty monthly expiry on Thursdays and weekly expiries on
        # Wednesdays till 31st Mar, 2024
        if for_instrument.is_banknifty() and self.date < date(
            year=2024, month=3, day=1
        ):
            dow = for_instrument.expiry_dow + 1

        return is_last_weekday_of_the_month(on_date=self.date, weekday=dow)

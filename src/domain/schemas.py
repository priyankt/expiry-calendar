from typing import Optional, List
from datetime import date, timedelta
from pydantic import BaseModel

from src.lib.common import is_last_thursday_of_the_month


class Instrument(BaseModel):
    name: str
    lot_size: int
    expiry_dow: int

    def is_expiring(self, on_date: date) -> bool:
        """
        Returns if the instrument is expiring on a given date

        Args:
            on_date: datetime.date

        Returns:
            True if the instrument is expiring, False otherwise
        """
        if not self.is_banknifty():
            return self.expiry_dow == on_date.weekday()

        return self.is_banknifty_expiring(on_date=on_date)

    def is_banknifty(self) -> bool:
        """
        Returns if the instrument is a bank nifty instrument

        Args:
            on_date: datetime.date

        Returns:
            True if the instrument is banknifty, False otherwise
        """
        return self.name.lower().startswith("banknifty")

    def is_banknifty_expiring(self, on_date: date) -> bool:
        """
        The weekly expiry of banknifty is on wednesday and monthly
        banknifty expiry is on Thursday till 31st Mar, 2024

        Args:
            on_date: datetime.date

        Returns:
            True if banknifty weekly expiry on wednesday or
            monthly expiry on Thursday
        """
        if not self.is_banknifty():
            return False
        if on_date > date(year=2024, month=3, day=31):
            return self.expiry_dow == on_date.weekday()
        # Instrument is banknifty before 31st Mar, 2024
        # & last thursday of the month
        if is_last_thursday_of_the_month(on_date=on_date):
            return True
        # If its a wednesday and tomorrow is the last thursday of the month
        # then monthly expiry will be tomorrow so no expiry today
        return (
            self.expiry_dow == on_date.weekday()
            and not is_last_thursday_of_the_month(on_date=on_date + timedelta(days=1))
        )

    def __lt__(self, other: "Instrument") -> bool:
        return self.name < other.name


class Holiday(BaseModel):
    date: date
    description: Optional[str] = None


class Exchange(BaseModel):
    name: str
    holidays: List[Holiday]
    instruments: List[Instrument]

    def is_holiday(self, on_date: date) -> bool:
        """
        Returns if its a holiday on a given date

        Args:
            on_date: datetime.date

        Returns:
            True if its a holiday, False otherwise
        """
        return on_date in self

    def expiring_instruments(
        self, on_date: date, ignore_holiday: bool = False
    ) -> List[Instrument]:
        """
        Returns all instruments that are expiring on a given date.
        Moves up the expiry if the next business day is a holiday.

        Args:
            on_date: datetime.date

        Returns:
            List of expiring instruments
        """
        if (
            not ignore_holiday and self.is_holiday(on_date=on_date)
        ) or on_date.weekday() > 4:
            return []
        expiring_instruments: List[Instrument] = list(
            filter(lambda x: x.is_expiring(on_date=on_date), self.instruments)
        )
        next_business_date: date = self.next_business_date(after_date=on_date)
        if self.is_holiday(on_date=next_business_date):
            expiring_instruments.extend(
                self.expiring_instruments(
                    on_date=next_business_date, ignore_holiday=True
                )
            )

        return expiring_instruments

    def next_trading_date(self, after_date: date) -> date:
        """
        Returns next trading date. excludes weekends & holidays.

        Args:
            after_date: datetime.date

        Returns:
            datetime.date
        """
        next_trading_date: date = self.next_business_date(after_date=after_date)
        while self.is_holiday(on_date=next_trading_date):
            next_trading_date = self.next_business_date(after_date=next_trading_date)

        return next_trading_date

    def next_business_date(self, after_date: date) -> date:
        """
        Returns next working date. Weekends excluded. Holidays not.

        Args:
            after_date: datetime.date

        Returns:
            datetime.date
        """
        next_date: date = after_date + timedelta(days=1)
        # weekday() -> Monday == 0 ... Sunday == 6.
        while next_date.weekday() > 4:
            next_date += timedelta(days=1)

        return next_date

    def __contains__(self, date: date) -> bool:
        return date in map(lambda x: x.date, self.holidays)


class Market(BaseModel):
    exchanges: List[Exchange]

    def expiring_instruments(self, on_date: date) -> List[Instrument]:
        """
        Returns all the instruments across all exchanges that are expiring on a given date.

        Args:
            on_date: datetime.date

        Returns:
            List[Instrument]
        """
        expiring_instruments: List[Instrument] = []
        for exchange in self.exchanges:
            expiring_instruments.extend(exchange.expiring_instruments(on_date=on_date))

        return expiring_instruments

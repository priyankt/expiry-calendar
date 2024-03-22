import locale
import time
from typing import List, Optional
from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from dotenv import load_dotenv

from src.domain.schemas import Market
from src.ui.schemas import ExpirySection

load_dotenv()

from src.config import LOCALE_STR
from src.lib.repos import get_market
from src.lib.common import get_cache_expiry_seconds, get_today
from src.lib.database import SessionLocal

app = FastAPI()
app.mount(path="/assets", app=StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
templates.env.globals["css_version"] = time.time_ns()  # type: ignore
locale.setlocale(category=locale.LC_ALL, locale=LOCALE_STR)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(path="/", response_class=HTMLResponse)
async def get_expiry_calendar(
    request: Request, today: Optional[date] = None, db: Session = Depends(get_db)
):
    if today is None:
        today = get_today()
    market: Market = get_market(db=db)
    end_date: date = today + timedelta(days=7)
    expiry_sections: List[ExpirySection] = []
    is_selected = True
    while today < end_date:
        expiry_sections.append(
            ExpirySection(
                date=today,
                instruments=market.expiring_instruments(on_date=today),
                is_selected=is_selected,
            )
        )
        is_selected = False
        today += timedelta(days=1)

    cache_secs: int = get_cache_expiry_seconds(
        now=datetime.now(tz=ZoneInfo(key="Asia/Calcutta"))
    )
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "expiry_sections": expiry_sections},
        headers={"cache-control": f"max-age={cache_secs}, public"},
    )

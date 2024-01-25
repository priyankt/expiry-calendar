import locale
import time
from typing import List
from datetime import date, timedelta

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from dotenv import load_dotenv

from src.domain.schemas import Market
from src.ui.schemas import ExpirySection

load_dotenv()

from src.config import LOCALE_STR, logger
from src.lib.repos import get_market

app = FastAPI()
app.mount(path="/assets", app=StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
templates.env.globals["css_version"] = time.time_ns()
locale.setlocale(category=locale.LC_ALL, locale=LOCALE_STR)


@app.get(path="/", response_class=HTMLResponse)
async def get_expiry_calendar(request: Request, today: date = date.today()):
    market: Market = get_market()
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

    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "expiry_sections": expiry_sections},
    )

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from .database import init_db, get_db
from .models import CurrencyRates, StatsResponse
from .services import fetch_rates
from datetime import datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/rates", status_code=302)


@app.get("/rates", response_model=CurrencyRates)
async def get_current_rates():
    try:
        rates = await fetch_rates()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    async with get_db() as db:
        await db.execute(
            "INSERT INTO rate_requests (usd, eur, gbp, jpy, chf) VALUES (?, ?, ?, ?, ?)",
            (rates["usd"], rates["eur"],
             rates["gbp"], rates["jpy"], rates["chf"])
        )
        await db.commit()

    return CurrencyRates(
        usd=round(rates["usd"], 2),
        eur=round(rates["eur"], 2),
        gbp=round(rates["gbp"], 2),
        jpy=round(rates["jpy"], 2),
        chf=round(rates["chf"], 2),
        timestamp=datetime.now()
    )


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    async with get_db() as db:
        total = await db.execute("SELECT COUNT(*) as cnt FROM rate_requests")
        total_count = (await total.fetchone())["cnt"]
        avg = await db.execute(
            "SELECT AVG(usd) as avg_usd, AVG(eur) as avg_eur, "
            "AVG(gbp) as avg_gbp, AVG(jpy) as avg_jpy, AVG(chf) as avg_chf "
            "FROM rate_requests"
        )
        avg_row = await avg.fetchone()
        average_rates = {
            "usd": avg_row["avg_usd"] or 0.0,
            "eur": avg_row["avg_eur"] or 0.0,
            "gbp": avg_row["avg_gbp"] or 0.0,
            "jpy": avg_row["avg_jpy"] or 0.0,
            "chf": avg_row["avg_chf"] or 0.0,
        }
        last = await db.execute(
            "SELECT usd, eur, gbp, jpy, chf, timestamp FROM rate_requests "
            "ORDER BY timestamp DESC LIMIT 10"
        )
        rows = await last.fetchall()
        last_requests = [
            CurrencyRates(
                usd=r["usd"],
                eur=r["eur"],
                gbp=r["gbp"],
                jpy=r["jpy"],
                chf=r["chf"],
                timestamp=datetime.fromisoformat(
                    r["timestamp"])
            )
            for r in rows
        ]
    return StatsResponse(
        total_requests=total_count,
        average_rates=average_rates,
        last_requests=last_requests
    )

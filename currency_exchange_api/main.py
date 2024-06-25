import httpx
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import date, datetime
from models import Base, SessionLocal, ExchangeRate, engine
import redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import aioredis

app = FastAPI()


redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fetch from Frankfurter API
async def fetch_exchange_rate():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.frankfurter.app/latest?from=USD&to=EUR")
        response.raise_for_status()
        data = response.json()
        return data['rates']['EUR']

# Fetch from cache or API
async def fetch_exchange_rate_from_cache():
    rate = redis_client.get("usd_to_eur_rate")
    if rate:
        return float(rate)
    rate_value = await fetch_exchange_rate()
    redis_client.setex("usd_to_eur_rate", 3600, rate_value)
    return rate_value

# Fetch and store in background
async def fetch_and_store_rate(today, db):
    rate_value = await fetch_exchange_rate_from_cache()
    rate = ExchangeRate(date=today, usd_to_eur_rate=rate_value)
    db.add(rate)
    db.commit()

# Endpoint - today's rate
@app.get("/rate")
async def get_rate(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    today = date.today()
    rate = db.query(ExchangeRate).filter(ExchangeRate.date == today).first()
    if not rate:
        background_tasks.add_task(fetch_and_store_rate, today, db)
        return {"date": today, "usd_to_eur_rate": "Fetching..."}
    return {"date": today, "usd_to_eur_rate": rate.usd_to_eur_rate}

# Endpoint to get date range
@app.get("/rate/average")
async def get_average_rate(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    rates = db.query(ExchangeRate).filter(ExchangeRate.date.between(start, end)).all()
    if not rates:
        raise HTTPException(status_code=404, detail="No data available for the given date range")

    avg_rate = sum(rate.usd_to_eur_rate for rate in rates) / len(rates)
    return {"start_date": start_date, "end_date": end_date, "average_usd_to_eur_rate": avg_rate}

#Rate limiter
@app.lifespan("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)

@app.get("/rate", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def get_rate(db: Session = Depends(get_db)):
    # Endpoint
    today = date.today()
    rate = db.query(ExchangeRate).filter(ExchangeRate.date == today).first()
    if not rate:
        BackgroundTasks.add_task(fetch_and_store_rate, today, db)
        return {"date": today, "usd_to_eur_rate": "Fetching..."}
    return {"date": today, "usd_to_eur_rate": rate.usd_to_eur_rate}

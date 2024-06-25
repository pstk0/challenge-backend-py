from sqlalchemy import create_engine, Column, Float, Date, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Load configuration from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

DATABASE_URL = config["database_url"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    date = Column(Date, primary_key=True, index=True)
    usd_to_eur_rate = Column(Float, nullable=False)

Index('idx_date', ExchangeRate.date)

Base.metadata.create_all(bind=engine)

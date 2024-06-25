from fastapi.testclient import TestClient
from main import app, get_db
from models import Base, engine, SessionLocal
import json

client = TestClient(app)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_get_rate():
    response = client.get("/rate")
    assert response.status_code == 200
    assert "usd_to_eur_rate" in response.json()

def test_get_average_rate():
    response = client.get("/rate/average?start_date=2023-01-01&end_date=2023-01-31")
    assert response.status_code == 200
    assert "average_usd_to_eur_rate" in response.json()

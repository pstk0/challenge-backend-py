Bash logs, commands & comments on files created to keep track of workflow and how I choose to work.

$ mkdir currency_exchange_api
cd currency_exchange_api
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic requests httpx aioredis fastapi-limiter redis


models.py
Database Model
Define the database model for storing exchange rates.


main.py
FastAPI Application with Frankfurter API Integration
Create the main application file with endpoints and database session management.


test_main.py
Test the Endpoints
Write tests using FastAPI's TestClient to ensure everything works seamlessly.
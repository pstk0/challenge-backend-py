# challenge-backend-py
 Backend Developer Challenge - Darwin Interactive | Pedro Leal

This repository features a version of the challenge solution that takes a straightforward and easier approach to the problem than was originally proposed.

Bash logs, commands & comments on files created to keep track of workflow and how I choose to work.

$ mkdir currency_exchange_api
cd currency_exchange_api
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic requests httpx aioredis fastapi-limiter redis

currency_exchange_api/
│
├── venv/                   # Virtual environment (directory)
│
├── app/
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # Database models
│   └── test_main.py        # Test the Endpoints Write tests using FastAPI's (e.g., API fetch, caching)
├── config.json             # Configuration file
└── README.md               # Project README file

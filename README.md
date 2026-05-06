# Mini InsureTech QA Automation Portfolio

A QA-focused portfolio project for a mini InsureTech API built with FastAPI and tested with pytest.

The FastAPI application is intentionally small and exists only as the Software Under Test (SUT).  
The main purpose of this repository is to demonstrate backend API automation, integration testing, business rule validation, and data integrity checks.

## Current Scope

Implemented endpoints:

- `GET /health`
- `POST /customers`
- `GET /customers/{customer_id}`
- `POST /quotes`
- `GET /quotes/{quote_id}`

## Tech Stack

- Python
- FastAPI
- Pydantic
- pytest
- FastAPI TestClient
- uv

## Run Tests

```bash
uv run pytest
```

## Run API

```bash
uv run uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Test Focus

Current tests cover positive, negative, integration, and business rule scenarios for Customer and Quote APIs.

Examples of covered scenarios:

- health check validation
- customer creation
- customer retrieval
- invalid customer input
- quote creation for an existing customer
- quote rejection for an unknown customer
- premium calculation validation
- quote retrieval
- negative API scenarios

## Planned Improvements

- Policy and Claim APIs
- richer error response handling
- duplicate email validation
- CI with GitHub Actions
- Postman collection
- lightweight UI automation with Playwright

from datetime import date, timedelta

from fastapi import FastAPI, HTTPException

from app.database import db
from app.models import Customer, Quote
from app.schemas import (
    CustomerCreateRequest,
    CustomerResponse,
    ErrorResponse,
    QuoteCreateRequest,
    QuoteResponse,
)
from app.services.quote_service import calculate_car_premium

app = FastAPI(title="Mini InsureTech QA Portfolio API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/customers",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(request: CustomerCreateRequest):
    customer_id = db.next_customer_id()

    customer = Customer(
        customer_id=customer_id,
        first_name=request.first_name,
        last_name=request.last_name,
        date_of_birth=request.date_of_birth,
        email=request.email,
    )

    db.customers[customer_id] = customer
    return customer


@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse,
    responses={
        404: {"model": ErrorResponse},
    },
)
def get_customer(customer_id: str):
    customer = db.customers.get(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "CUSTOMER_NOT_FOUND",
                "message": "Customer does not exist.",
            },
        )

    return customer


@app.post(
    "/quotes",
    response_model=QuoteResponse,
    status_code=201,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    },
)
def create_quote(request: QuoteCreateRequest):
    customer = db.customers.get(request.customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "CUSTOMER_NOT_FOUND",
                "message": "Customer does not exist.",
            },
        )

    if request.product_type != "car":
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "UNSUPPORTED_PRODUCT_TYPE",
                "message": "Only car quotes are supported.",
            },
        )

    premium = calculate_car_premium(
        vehicle_value=request.vehicle_value,
        postcode=request.postcode,
        driver_age=request.driver_age,
        has_previous_claims=request.has_previous_claims,
    )

    quote_id = db.next_quote_id()
    valid_until = date.today() + timedelta(days=30)

    quote = Quote(
        quote_id=quote_id,
        customer_id=request.customer_id,
        product_type=request.product_type,
        vehicle_value=request.vehicle_value,
        postcode=request.postcode,
        driver_age=request.driver_age,
        has_previous_claims=request.has_previous_claims,
        premium=premium,
        status="QUOTED",
        valid_until=valid_until,
    )

    db.quotes[quote_id] = quote
    return quote


@app.get(
    "/quotes/{quote_id}",
    response_model=QuoteResponse,
    responses={
        404: {"model": ErrorResponse},
    },
)
def get_quote(quote_id: str):
    quote = db.quotes.get(quote_id)

    if not quote:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "QUOTE_NOT_FOUND",
                "message": "Quote does not exist.",
            },
        )

    return quote

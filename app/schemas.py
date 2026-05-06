from datetime import date
from pydantic import BaseModel, EmailStr, Field


class CustomerCreateRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    date_of_birth: date
    email: EmailStr


class CustomerResponse(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr


class QuoteCreateRequest(BaseModel):
    customer_id: str
    product_type: str
    vehicle_value: float = Field(gt=0)
    postcode: str = Field(min_length=4, max_length=4)
    driver_age: int = Field(ge=18)
    has_previous_claims: bool


class QuoteResponse(BaseModel):
    quote_id: str
    customer_id: str
    product_type: str
    vehicle_value: float
    postcode: str
    driver_age: int
    has_previous_claims: bool
    premium: float
    status: str
    valid_until: date


class ErrorResponse(BaseModel):
    error_code: str
    message: str

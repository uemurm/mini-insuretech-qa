from dataclasses import dataclass
from datetime import date


@dataclass
class Customer:
    customer_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: str


@dataclass
class Quote:
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

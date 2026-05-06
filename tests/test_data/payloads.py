def valid_customer_payload(**overrides):
    payload = {
        "first_name": "Taro",
        "last_name": "Yamada",
        "date_of_birth": "1990-05-10",
        "email": "taro.yamada@example.com",
    }
    payload.update(overrides)
    return payload


def valid_quote_payload(**overrides):
    payload = {
        "customer_id": "cus_001",
        "product_type": "car",
        "vehicle_value": 30000,
        "postcode": "2000",
        "driver_age": 35,
        "has_previous_claims": False,
    }
    payload.update(overrides)
    return payload

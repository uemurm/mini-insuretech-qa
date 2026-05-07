from datetime import date, timedelta

import pytest

from tests.test_data.payloads import valid_customer_payload, valid_quote_payload


def test_create_quote_for_existing_customer_returns_201(client):
    customer_response = client.post("/customers", json=valid_customer_payload())
    customer_id = customer_response.json()["customer_id"]

    payload = valid_quote_payload(customer_id=customer_id)
    response = client.post("/quotes", json=payload)

    assert response.status_code == 201

    body = response.json()
    assert body["quote_id"] == "quo_001"
    assert body["customer_id"] == customer_id
    assert body["product_type"] == "car"
    assert body["status"] == "QUOTED"


def test_create_quote_rejects_unknown_customer(client):
    payload = valid_quote_payload(customer_id="cus_999")

    response = client.post("/quotes", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "CUSTOMER_NOT_FOUND"
    assert response.json()["detail"]["message"] == "Customer does not exist."


def assert_premium(client, expected_premium, **quote_overrides):
    customer_response = client.post("/customers", json=valid_customer_payload())
    customer_id = customer_response.json()["customer_id"]
    quote_overrides.update({"customer_id": customer_id})

    payload = valid_quote_payload(**quote_overrides)

    response = client.post("/quotes", json=payload)

    assert response.status_code == 201
    assert response.json()["premium"] == expected_premium


def test_create_quote_calculates_premium_correctly(client):
    assert_premium(client, 800.0)


@pytest.mark.parametrize("age, expected_premium", [
    (24, 1100.0),
    (25,  800.0),
])
def test_create_quote_calculates_premium_with_varied_ages(client, age, expected_premium):
    assert_premium(client, expected_premium, driver_age=age)


@pytest.mark.parametrize("postcode, expected_premium", [
    ('1000', 750.0),
    ('2000', 800.0),
])
def test_create_quote_calculates_premium_with_varied_postcodes(client, postcode, expected_premium):
    assert_premium(client, expected_premium, postcode=postcode)


@pytest.mark.parametrize("has_previous_claims, expected_premium", [
    (False, 750.0),
    (True,  950.0),
])
def test_create_quote_calculates_premium_with_varied_previous_claims(client, has_previous_claims, expected_premium):
    assert_premium(client, expected_premium, has_previous_claims=has_previous_claims, postcode='1000')


def test_get_quote_returns_created_quote(client):
    customer_response = client.post("/customers", json=valid_customer_payload())
    customer_id = customer_response.json()["customer_id"]

    create_quote_response = client.post(
        "/quotes",
        json=valid_quote_payload(customer_id=customer_id),
    )
    quote_id = create_quote_response.json()["quote_id"]

    response = client.get(f"/quotes/{quote_id}")

    assert response.status_code == 200
    assert response.json()["quote_id"] == quote_id
    assert response.json()["customer_id"] == customer_id


def test_get_unknown_quote_returns_404(client):
    response = client.get("/quotes/quo_999")

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "QUOTE_NOT_FOUND"
    assert response.json()["detail"]["message"] == "Quote does not exist."


def test_create_quote_sets_valid_until_to_30_days_from_today(client):
    customer_response = client.post("/customers", json=valid_customer_payload())
    customer_id = customer_response.json()["customer_id"]

    response = client.post(
        "/quotes",
        json=valid_quote_payload(customer_id=customer_id),
    )

    assert response.status_code == 201
    expected_date = (date.today() + timedelta(days=30)).isoformat()
    assert response.json()["valid_until"] == expected_date


def test_create_quote_applies_minimum_premium_rule(client):
    customer_response = client.post("/customers", json=valid_customer_payload())
    customer_id = customer_response.json()["customer_id"]

    response = client.post(
        "/quotes",
        json=valid_quote_payload(
            customer_id=customer_id,
            vehicle_value=10000,
            postcode="3000",
            driver_age=35,
            has_previous_claims=False,
        ),
    )

    assert response.status_code == 201
    assert response.json()["premium"] == 500.0


def test_create_quote_rejects_underage_driver(client):
    customer_response = client.post("/customers", json=valid_customer_payload())
    customer_id = customer_response.json()["customer_id"]

    response = client.post(
        "/quotes",
        json=valid_quote_payload(customer_id=customer_id, driver_age=17),
    )

    assert response.status_code == 422

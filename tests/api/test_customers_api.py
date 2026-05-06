from tests.test_data.payloads import valid_customer_payload


def test_create_customer_returns_201(client):
    response = client.post("/customers", json=valid_customer_payload())

    assert response.status_code == 201

    body = response.json()
    assert body["customer_id"] == "cus_001"
    assert body["first_name"] == "Taro"
    assert body["last_name"] == "Yamada"
    assert body["date_of_birth"] == "1990-05-10"
    assert body["email"] == "taro.yamada@example.com"


def test_create_customer_rejects_invalid_email(client):
    payload = valid_customer_payload(email="not-an-email")

    response = client.post("/customers", json=payload)

    assert response.status_code == 422


def test_get_customer_returns_created_customer(client):
    create_response = client.post("/customers", json=valid_customer_payload())
    customer_id = create_response.json()["customer_id"]

    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == 200

    body = response.json()
    assert body["customer_id"] == customer_id
    assert body["email"] == "taro.yamada@example.com"


def test_get_unknown_customer_returns_404(client):
    response = client.get("/customers/cus_999")

    assert response.status_code == 404
    assert response.json()["detail"]["error_code"] == "CUSTOMER_NOT_FOUND"
    assert response.json()["detail"]["message"] == "Customer does not exist."


def test_create_customer_rejects_empty_first_name(client):
    payload = valid_customer_payload(first_name="")

    response = client.post("/customers", json=payload)

    assert response.status_code == 422

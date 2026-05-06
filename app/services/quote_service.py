def calculate_car_premium(
    vehicle_value: float,
    postcode: str,
    driver_age: int,
    has_previous_claims: bool,
) -> float:
    premium = vehicle_value * 0.025

    if driver_age < 25:
        premium += 300

    if postcode.startswith("2"):
        premium += 50

    if has_previous_claims:
        premium += 200

    if premium < 500:
        premium = 500

    return float(premium)

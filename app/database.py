from app.models import Customer, Quote


class InMemoryDatabase:
    def __init__(self):
        self.customers: dict[str, Customer] = {}
        self.quotes: dict[str, Quote] = {}
        self.customer_sequence = 1
        self.quote_sequence = 1

    def reset(self):
        self.customers.clear()
        self.quotes.clear()
        self.customer_sequence = 1
        self.quote_sequence = 1

    def next_customer_id(self) -> str:
        customer_id = f"cus_{self.customer_sequence:03d}"
        self.customer_sequence += 1
        return customer_id

    def next_quote_id(self) -> str:
        quote_id = f"quo_{self.quote_sequence:03d}"
        self.quote_sequence += 1
        return quote_id


db = InMemoryDatabase()

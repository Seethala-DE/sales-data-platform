"""Generate fake source data: customers (CSV), products (JSON), sales (CSV)."""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

SEED = 42
N_CUSTOMERS = 5000
N_PRODUCTS = 500
N_SALES = 100000

OUT_DIR = Path("data/source")
OUT_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker("en_IN")
Faker.seed(SEED)
random.seed(SEED)

CATEGORIES = {
    "Electronics": ["Headphones", "Keyboard", "Mouse", "Monitor", "Webcam", "Speaker"],
    "Home": ["Lamp", "Cushion", "Kettle", "Clock", "Organizer", "Mug"],
    "Clothing": ["T-Shirt", "Jacket", "Jeans", "Cap", "Socks", "Hoodie"],
    "Sports": ["Yoga Mat", "Dumbbell", "Football", "Bottle", "Skipping Rope", "Racket"],
}


def make_customers(n):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "customer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "state": fake.state(),
            "segment": random.choice(["Retail", "Corporate", "Small Business"]),
            "signup_date": fake.date_between(start_date="-3y", end_date="today"),
        })
    return pd.DataFrame(rows)


def make_products(n):
    products = []
    for i in range(1, n + 1):
        category = random.choice(list(CATEGORIES))
        item = random.choice(CATEGORIES[category])
        cost = round(random.uniform(200, 5000), 2)
        price = round(cost * random.uniform(1.2, 1.8), 2)
        products.append({
            "product_id": i,
            "product_name": f"{fake.word().title()} {item}",
            "category": category,
            "unit_cost": cost,
            "unit_price": price,
        })
    return products

SALES_CHANNELS = ["Online", "Mobile App", "Store", "Marketplace"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Shipped", "Processing", "Cancelled", "Returned"]
COUPON_CODES = ["WELCOME10", "FESTIVE15", "SAVE5", "FLASH20", None, None, None, None]
SHIPPING_CITIES = [fake.city() for _ in range(50)]

def make_sales(n, n_customers, products):
    start = datetime.now() - timedelta(days=365)
    # Sorted timestamps so sale_id increases with time (useful for incremental loads later)
    offsets = sorted(random.randint(0, 365 * 24 * 3600) for _ in range(n))
    rows = []
    for i, offset in enumerate(offsets, start=1):
        order_ts = start + timedelta(seconds=offset)
        product = random.choice(products)
        qty = random.randint(1, 5)
        discount = random.choice([0, 0, 0, 5, 10, 15])
        total = round(qty * product["unit_price"] * (1 - discount / 100), 2)
        rows.append({
            "sale_id": i,
            "order_number": f"ORD-{order_ts.year}-{i:06d}",
            "customer_id": random.randint(1, n_customers),
            "product_id": product["product_id"],
            "quantity": qty,
            "unit_price": product["unit_price"],
            "discount_pct": discount,
            "total_amount": total,
            "sales_channel": random.choice(SALES_CHANNELS),
            "payment_method": random.choice(PAYMENT_METHODS),
            "order_status": random.choice(ORDER_STATUSES),
            "shipping_city": random.choice(SHIPPING_CITIES),
            "coupon_code": random.choice(COUPON_CODES),
            "order_date": order_ts.date(),
            "updated_at": order_ts.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    customers = make_customers(N_CUSTOMERS)
    products = make_products(N_PRODUCTS)
    sales = make_sales(N_SALES, N_CUSTOMERS, products)

    customers.to_csv(OUT_DIR / "customers.csv", index=False)
    with open(OUT_DIR / "products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)
    sales.to_csv(OUT_DIR / "sales.csv", index=False)

    print(f"customers: {len(customers)} rows")
    print(f"products:  {len(products)} rows")
    print(f"sales:     {len(sales)} rows")
    print(f"Files saved in {OUT_DIR.resolve()}")
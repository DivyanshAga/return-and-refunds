import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------

random.seed(42)
np.random.seed(42)

NUM_ORDERS = 100_000
NUM_PRODUCTS = 2_000
NUM_SELLERS = 100
NUM_CUSTOMERS = 20_000

OUTPUT_DIR = "data/raw"


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


# -----------------------------
# 1. SELLERS
# -----------------------------

print("Generating sellers...")

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

sellers = []

for i in range(1, NUM_SELLERS + 1):

    sellers.append({
        "seller_id": f"SELL{i:04d}",
        "seller_name": f"Seller_{i:04d}",
        "seller_region": random.choice(regions),
        "seller_rating": round(random.uniform(2.5, 5.0), 2),
        "seller_join_date": random_date(
            datetime(2022, 1, 1),
            datetime(2025, 12, 31)
        ).date()
    })

sellers_df = pd.DataFrame(sellers)


# -----------------------------
# 2. PRODUCTS
# -----------------------------

print("Generating products...")

categories = {
    "Electronics": [
        "Mobiles",
        "Laptops",
        "Headphones",
        "Accessories"
    ],
    "Fashion": [
        "Mens Clothing",
        "Womens Clothing",
        "Shoes",
        "Bags"
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Decor",
        "Storage"
    ],
    "Beauty": [
        "Skincare",
        "Haircare",
        "Makeup"
    ],
    "Sports": [
        "Fitness",
        "Outdoor",
        "Sportswear"
    ]
}

brands = [
    "Nova",
    "UrbanX",
    "Prime",
    "Vertex",
    "Apex",
    "Zenith",
    "Core",
    "Pulse"
]

products = []

for i in range(1, NUM_PRODUCTS + 1):

    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])

    cost_price = round(random.uniform(100, 20_000), 2)

    # Selling price is generally higher than cost
    selling_price = round(
        cost_price * random.uniform(1.10, 1.80),
        2
    )

    products.append({
        "product_id": f"PROD{i:05d}",
        "product_name": f"{random.choice(brands)} {subcategory} Product {i}",
        "category": category,
        "subcategory": subcategory,
        "brand": random.choice(brands),
        "seller_id": random.choice(sellers_df["seller_id"].tolist()),
        "cost_price": cost_price,
        "selling_price": selling_price,
        "weight_grams": random.randint(50, 20_000)
    })

products_df = pd.DataFrame(products)


# -----------------------------
# 3. CUSTOMERS
# -----------------------------

print("Generating customers...")

cities = [
    "Mumbai",
    "Pune",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Nashik"
]

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": f"CUST{i:05d}",
        "customer_name": f"Customer_{i:05d}",
        "city": random.choice(cities),
        "customer_segment": random.choice([
            "STANDARD",
            "PREMIUM",
            "VIP"
        ])
    })

customers_df = pd.DataFrame(customers)


# -----------------------------
# 4. ORDERS
# -----------------------------

print("Generating orders...")

order_statuses = [
    "DELIVERED",
    "DELIVERED",
    "DELIVERED",
    "DELIVERED",
    "CANCELLED"
]

payment_methods = [
    "UPI",
    "CREDIT_CARD",
    "DEBIT_CARD",
    "NET_BANKING",
    "COD"
]

orders = []

order_start = datetime(2026, 1, 1)
order_end = datetime(2026, 6, 30)

product_ids = products_df["product_id"].tolist()
customer_ids = customers_df["customer_id"].tolist()

# Product lookup for prices
product_price_lookup = products_df.set_index(
    "product_id"
)["selling_price"].to_dict()

product_seller_lookup = products_df.set_index(
    "product_id"
)["seller_id"].to_dict()

for i in range(1, NUM_ORDERS + 1):

    product_id = random.choice(product_ids)

    quantity = random.randint(1, 5)

    unit_price = product_price_lookup[product_id]

    # Discount between 0 and 20%
    discount = round(
        unit_price * quantity * random.uniform(0, 0.20),
        2
    )

    orders.append({
        "order_id": f"ORD{i:07d}",
        "customer_id": random.choice(customer_ids),
        "product_id": product_id,
        "seller_id": product_seller_lookup[product_id],
        "order_date": random_date(
            order_start,
            order_end
        ).date(),
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "payment_method": random.choice(payment_methods),
        "order_status": random.choice(order_statuses)
    })

orders_df = pd.DataFrame(orders)


# -----------------------------
# 5. RETURNS
# -----------------------------

print("Generating returns...")

return_reasons = [
    "DAMAGED",
    "WRONG_ITEM",
    "SIZE_ISSUE",
    "QUALITY_ISSUE",
    "CHANGED_MIND",
    "LATE_DELIVERY",
    "NOT_AS_DESCRIBED"
]

return_statuses = [
    "APPROVED",
    "APPROVED",
    "APPROVED",
    "REJECTED",
    "PENDING"
]

conditions = [
    "NEW",
    "USED",
    "DAMAGED",
    "OPENED"
]

# Only delivered orders can normally be returned
eligible_orders = orders_df[
    orders_df["order_status"] == "DELIVERED"
].copy()

# Roughly 12% of eligible orders become returns
num_returns = int(len(eligible_orders) * 0.12)

return_orders = eligible_orders.sample(
    n=num_returns,
    random_state=42
)

returns = []

for i, (_, order) in enumerate(return_orders.iterrows(), start=1):

    order_date = pd.Timestamp(order["order_date"])

    return_date = order_date + timedelta(
        days=random.randint(2, 30)
    )

    returns.append({
        "return_id": f"RET{i:06d}",
        "order_id": order["order_id"],
        "product_id": order["product_id"],
        "customer_id": order["customer_id"],
        "return_date": return_date.date(),
        "return_reason": random.choice(return_reasons),
        "return_quantity": random.randint(
            1,
            int(order["quantity"])
        ),
        "return_status": random.choice(return_statuses),
        "condition": random.choice(conditions)
    })

returns_df = pd.DataFrame(returns)


# -----------------------------
# 6. REFUNDS
# -----------------------------

print("Generating refunds...")

refund_methods = [
    "ORIGINAL_PAYMENT",
    "WALLET",
    "BANK_TRANSFER"
]

refund_statuses = [
    "COMPLETED",
    "COMPLETED",
    "COMPLETED",
    "PENDING",
    "FAILED"
]

refunds = []

# Only approved returns are eligible for refunds
approved_returns = returns_df[
    returns_df["return_status"] == "APPROVED"
].copy()

for i, (_, ret) in enumerate(
    approved_returns.iterrows(),
    start=1
):

    order = orders_df[
        orders_df["order_id"] == ret["order_id"]
    ].iloc[0]

    return_date = pd.Timestamp(ret["return_date"])

    refund_requested = return_date + timedelta(
        hours=random.randint(2, 48)
    )

    # Refund processing time:
    # Most refunds are fast, some intentionally slow
    processing_days = random.choices(
        [1, 2, 3, 4, 5, 8, 12],
        weights=[20, 25, 25, 15, 8, 5, 2]
    )[0]

    refund_processed = refund_requested + timedelta(
        days=processing_days,
        hours=random.randint(0, 12)
    )

    refund_amount = round(
        (
            order["unit_price"]
            * ret["return_quantity"]
        )
        - (
            order["discount"]
            / order["quantity"]
            * ret["return_quantity"]
        ),
        2
    )

    refunds.append({
        "refund_id": f"REF{i:06d}",
        "return_id": ret["return_id"],
        "order_id": ret["order_id"],
        "refund_requested_at": refund_requested,
        "refund_processed_at": refund_processed,
        "refund_amount": max(refund_amount, 0),
        "refund_status": random.choice(refund_statuses),
        "refund_method": random.choice(refund_methods)
    })

refunds_df = pd.DataFrame(refunds)


# -----------------------------
# 7. INTRODUCE DATA QUALITY ISSUES
# -----------------------------

print("Introducing data quality issues...")


# Duplicate orders
duplicate_orders = orders_df.sample(
    n=100,
    random_state=10
)

orders_df = pd.concat(
    [orders_df, duplicate_orders],
    ignore_index=True
)


# Missing customer IDs
missing_customer_indices = orders_df.sample(
    n=200,
    random_state=11
).index

orders_df.loc[
    missing_customer_indices,
    "customer_id"
] = None


# Different casing in return reasons
if len(returns_df) > 0:

    returns_df.loc[
        returns_df.sample(
            n=min(100, len(returns_df)),
            random_state=12
        ).index,
        "return_reason"
    ] = "damaged"


# Invalid quantities
invalid_quantity_indices = orders_df.sample(
    n=50,
    random_state=13
).index

orders_df.loc[
    invalid_quantity_indices,
    "quantity"
] = 0


# Duplicate returns
duplicate_returns = returns_df.sample(
    n=min(50, len(returns_df)),
    random_state=14
)

returns_df = pd.concat(
    [returns_df, duplicate_returns],
    ignore_index=True
)


# -----------------------------
# 8. SAVE DATA
# -----------------------------

import os

os.makedirs(OUTPUT_DIR, exist_ok=True)

sellers_df.to_csv(
    f"{OUTPUT_DIR}/sellers.csv",
    index=False
)

products_df.to_csv(
    f"{OUTPUT_DIR}/products.csv",
    index=False
)

customers_df.to_csv(
    f"{OUTPUT_DIR}/customers.csv",
    index=False
)

orders_df.to_csv(
    f"{OUTPUT_DIR}/orders.csv",
    index=False
)

returns_df.to_csv(
    f"{OUTPUT_DIR}/returns.csv",
    index=False
)

refunds_df.to_csv(
    f"{OUTPUT_DIR}/refunds.csv",
    index=False
)


# -----------------------------
# 9. SUMMARY
# -----------------------------

print("\nData generation complete!")

print(f"Customers : {len(customers_df):,}")
print(f"Sellers   : {len(sellers_df):,}")
print(f"Products  : {len(products_df):,}")
print(f"Orders    : {len(orders_df):,}")
print(f"Returns   : {len(returns_df):,}")
print(f"Refunds   : {len(refunds_df):,}")

print("\nFiles created in:")
print(OUTPUT_DIR)
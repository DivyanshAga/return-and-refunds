import pandas as pd
import os

DATA_DIR = "data/raw"


# -----------------------------
# LOAD DATA
# -----------------------------

customers = pd.read_csv(f"{DATA_DIR}/customers.csv")
sellers = pd.read_csv(f"{DATA_DIR}/sellers.csv")
products = pd.read_csv(f"{DATA_DIR}/products.csv")
orders = pd.read_csv(f"{DATA_DIR}/orders.csv")
returns = pd.read_csv(f"{DATA_DIR}/returns.csv")
refunds = pd.read_csv(f"{DATA_DIR}/refunds.csv")


# -----------------------------
# BASIC INFORMATION
# -----------------------------

print("\n========== DATASET SIZES ==========")

print(f"Customers : {len(customers):,}")
print(f"Sellers   : {len(sellers):,}")
print(f"Products  : {len(products):,}")
print(f"Orders    : {len(orders):,}")
print(f"Returns   : {len(returns):,}")
print(f"Refunds   : {len(refunds):,}")


# -----------------------------
# COLUMN INFORMATION
# -----------------------------

print("\n========== ORDERS COLUMNS ==========")
print(orders.columns.tolist())

print("\n========== RETURNS COLUMNS ==========")
print(returns.columns.tolist())

print("\n========== REFUNDS COLUMNS ==========")
print(refunds.columns.tolist())


# -----------------------------
# SAMPLE DATA
# -----------------------------

print("\n========== ORDERS SAMPLE ==========")
print(orders.head())

print("\n========== RETURNS SAMPLE ==========")
print(returns.head())

print("\n========== REFUNDS SAMPLE ==========")
print(refunds.head())


# -----------------------------
# NULL VALUES
# -----------------------------

print("\n========== NULL VALUES ==========")

print("\nOrders:")
print(orders.isnull().sum())

print("\nReturns:")
print(returns.isnull().sum())

print("\nRefunds:")
print(refunds.isnull().sum())


# -----------------------------
# DUPLICATES
# -----------------------------

print("\n========== DUPLICATES ==========")

print(
    "Duplicate orders:",
    orders["order_id"].duplicated().sum()
)

print(
    "Duplicate returns:",
    returns["return_id"].duplicated().sum()
)

print(
    "Duplicate refunds:",
    refunds["refund_id"].duplicated().sum()
)


# -----------------------------
# INVALID QUANTITIES
# -----------------------------

print("\n========== INVALID QUANTITIES ==========")

print(
    "Orders with quantity <= 0:",
    (orders["quantity"] <= 0).sum()
)

print(
    "Returns with quantity <= 0:",
    (returns["return_quantity"] <= 0).sum()
)


# -----------------------------
# RETURN DATE VALIDATION
# -----------------------------

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

returns["return_date"] = pd.to_datetime(
    returns["return_date"]
)

return_check = returns.merge(
    orders[
        [
            "order_id",
            "order_date"
        ]
    ].drop_duplicates("order_id"),
    on="order_id",
    how="left"
)

invalid_return_dates = return_check[
    return_check["return_date"]
    <
    return_check["order_date"]
]

print(
    "Returns before order date:",
    len(invalid_return_dates)
)


# -----------------------------
# ORPHAN RETURNS
# -----------------------------

orphan_returns = returns[
    ~returns["order_id"].isin(
        orders["order_id"]
    )
]

print(
    "Returns with unknown order_id:",
    len(orphan_returns)
)


# -----------------------------
# ORPHAN REFUNDS
# -----------------------------

orphan_refunds = refunds[
    ~refunds["return_id"].isin(
        returns["return_id"]
    )
]

print(
    "Refunds with unknown return_id:",
    len(orphan_refunds)
)


# -----------------------------
# RETURN REASONS
# -----------------------------

print("\n========== RETURN REASONS ==========")

print(
    returns["return_reason"]
    .value_counts(dropna=False)
)


# -----------------------------
# ORDER STATUS
# -----------------------------

print("\n========== ORDER STATUS ==========")

print(
    orders["order_status"]
    .value_counts(dropna=False)
)


# -----------------------------
# REFUND STATUS
# -----------------------------

print("\n========== REFUND STATUS ==========")

print(
    refunds["refund_status"]
    .value_counts(dropna=False)
)


# -----------------------------
# REFUND PROCESSING TIME
# -----------------------------

refunds["refund_requested_at"] = pd.to_datetime(
    refunds["refund_requested_at"]
)

refunds["refund_processed_at"] = pd.to_datetime(
    refunds["refund_processed_at"]
)

refunds["processing_days"] = (
    refunds["refund_processed_at"]
    - refunds["refund_requested_at"]
).dt.total_seconds() / 86400

print("\n========== REFUND PROCESSING TIME ==========")

print(
    refunds["processing_days"].describe()
)


# -----------------------------
# RELATIONSHIP CHECK
# -----------------------------

print("\n========== RELATIONSHIP CHECK ==========")

print(
    "Orders with valid customers:",
    orders["customer_id"]
    .isin(customers["customer_id"])
    .sum()
)

print(
    "Orders with valid products:",
    orders["product_id"]
    .isin(products["product_id"])
    .sum()
)

print(
    "Orders with valid sellers:",
    orders["seller_id"]
    .isin(sellers["seller_id"])
    .sum()
)


print("\n========== VALIDATION COMPLETE ==========")
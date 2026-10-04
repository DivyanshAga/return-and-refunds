-- SQL Query Optimization Example
-- Goal: identify high-value orders with customer information

-- BEFORE OPTIMIZATION
-- Uses SELECT * and filters after joining.

SELECT *
FROM ecommerce_returns.gold.fact_orders o
JOIN ecommerce_returns.gold.dim_customer c
    ON o.customer_id = c.customer_id
WHERE o.quantity > 2
  AND o.unit_price > 10000;


-- AFTER OPTIMIZATION
-- Select only required columns and filter orders before the join.

SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.quantity,
    o.unit_price,
    c.customer_name
FROM (
    SELECT
        order_id,
        customer_id,
        product_id,
        quantity,
        unit_price
    FROM ecommerce_returns.gold.fact_orders
    WHERE quantity > 2
      AND unit_price > 10000
) o
JOIN ecommerce_returns.gold.dim_customer c
    ON o.customer_id = c.customer_id;

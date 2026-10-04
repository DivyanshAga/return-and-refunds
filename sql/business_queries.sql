-- Business Query 1: Overall Return Rate

SELECT
    COUNT(DISTINCT r.return_id) AS total_returns,
    COUNT(DISTINCT r.order_id) AS returned_orders,
    COUNT(DISTINCT r.order_id) * 100.0
        / COUNT(DISTINCT o.order_id) AS return_rate
FROM ecommerce_returns.gold.fact_returns r
CROSS JOIN (
    SELECT COUNT(DISTINCT order_id) AS order_count
    FROM ecommerce_returns.gold.fact_orders
) o;


-- Business Query 2: Top Returned Products

SELECT
    product_id,
    SUM(total_returns) AS total_returns
FROM ecommerce_returns.gold.product_return_metrics
GROUP BY product_id
ORDER BY total_returns DESC
LIMIT 10;


-- Business Query 3: Top Returned Categories

SELECT
    category,
    SUM(total_returns) AS total_returns
FROM ecommerce_returns.gold.vw_top_returned_categories
GROUP BY category
ORDER BY total_returns DESC;


-- Business Query 4: Seller Return Rates

SELECT
    seller_id,
    total_orders,
    total_returns,
    return_rate
FROM ecommerce_returns.gold.vw_seller_return_rates
ORDER BY return_rate DESC
LIMIT 10;


-- Business Query 5: Monthly Return Trend

SELECT
    return_month,
    total_returns
FROM ecommerce_returns.gold.vw_monthly_return_trend
ORDER BY return_month;


-- Business Query 6: Return Reasons

SELECT
    return_reason,
    total_returns,
    total_returned_quantity
FROM ecommerce_returns.gold.vw_return_reasons
ORDER BY total_returns DESC;


-- Business Query 7: Refund Metrics

SELECT
    total_refunds,
    total_refund_amount,
    avg_refund_processing_days,
    refund_sla_breaches,
    refund_sla_breach_rate
FROM ecommerce_returns.gold.vw_business_kpis;

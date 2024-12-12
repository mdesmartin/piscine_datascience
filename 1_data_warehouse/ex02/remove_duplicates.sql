CREATE TABLE customers_deduplicated AS
WITH ranked_customers AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY event_type, product_id, price, user_id, user_session
            ORDER BY event_time
        ) AS rn,
        LAG(event_time) OVER (
            PARTITION BY event_type, product_id, price, user_id, user_session
            ORDER BY event_time
        ) AS prev_event_time
    FROM customers
)
SELECT
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
FROM ranked_customers
WHERE rn = 1 OR (rn > 1 AND event_time - prev_event_time > interval '1 minute');

DROP TABLE customers;
ALTER TABLE customers_deduplicated RENAME TO customers;

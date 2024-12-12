ALTER TABLE customers
ADD COLUMN category_id BIGINT,
ADD COLUMN category_code VARCHAR(255),
ADD COLUMN brand VARCHAR(255);

UPDATE customers
SET
    category_id = i.category_id,
    category_code = i.category_code,
    brand = i.brand
FROM
    items i
WHERE
    customers.product_id = i.product_id;

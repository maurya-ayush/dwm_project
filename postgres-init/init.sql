CREATE TABLE IF NOT EXISTS raw_sales (
    transaction_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    sale_amount NUMERIC,
    sale_date DATE,
    region VARCHAR(50),
    discount NUMERIC
);

CREATE TABLE IF NOT EXISTS clean_sales (LIKE raw_sales);
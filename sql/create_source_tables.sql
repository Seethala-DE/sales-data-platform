DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    first_name    VARCHAR(100),
    last_name     VARCHAR(100),
    email         VARCHAR(255),
    phone         VARCHAR(50),
    city          VARCHAR(100),
    state         VARCHAR(100),
    segment       VARCHAR(50),
    signup_date   DATE
);

CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    product_name  VARCHAR(200),
    category      VARCHAR(100),
    unit_cost     NUMERIC(12,2),
    unit_price    NUMERIC(12,2)
);

CREATE TABLE sales (
    sale_id         INTEGER PRIMARY KEY,
    order_number    VARCHAR(30),
    customer_id     INTEGER REFERENCES customers(customer_id),
    product_id      INTEGER REFERENCES products(product_id),
    quantity        INTEGER,
    unit_price      NUMERIC(12,2),
    discount_pct    INTEGER,
    total_amount    NUMERIC(14,2),
    sales_channel   VARCHAR(30),
    payment_method  VARCHAR(30),
    order_status    VARCHAR(20),
    shipping_city   VARCHAR(100),
    coupon_code     VARCHAR(20),
    order_date      DATE,
    updated_at      TIMESTAMP
);
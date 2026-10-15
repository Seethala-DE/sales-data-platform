# Source Schemas

## customers.csv (CSV, 5,000 rows, 9 columns)
| Column | Type | Description |
|---|---|---|
| customer_id | int | Primary key |
| first_name | text | Customer first name |
| last_name | text | Customer last name |
| email | text | Email address |
| phone | text | Phone number (read as text to keep formatting) |
| city | text | City of residence |
| state | text | State of residence |
| segment | text | Retail, Corporate or Small Business |
| signup_date | date (text in CSV) | Date the customer signed up |

## products.json (JSON, 500 rows, 5 columns)
| Column | Type | Description |
|---|---|---|
| product_id | int | Primary key |
| product_name | text | Product name |
| category | text | Electronics, Home, Clothing or Sports |
| unit_cost | decimal | Cost to the business |
| unit_price | decimal | Selling price |

## sales.csv (CSV, 100,000 rows, 15 columns)
| Column | Type | Description |
|---|---|---|
| sale_id | int | Primary key |
| order_number | text | Business order reference, e.g. ORD-2025-000001 |
| customer_id | int | Foreign key to customers |
| product_id | int | Foreign key to products |
| quantity | int | Units sold (1 to 5) |
| unit_price | decimal | Price per unit at sale time |
| discount_pct | int | Discount percentage (0, 5, 10 or 15) |
| total_amount | decimal | quantity x unit_price after discount |
| sales_channel | text | Online, Mobile App, Store or Marketplace |
| payment_method | text | Card, UPI, Net Banking or Cash on Delivery |
| order_status | text | Delivered, Shipped, Processing, Cancelled or Returned |
| shipping_city | text | Destination city |
| coupon_code | text | Coupon used. Null for about 50% of orders |
| order_date | date (text in CSV) | Date of the order |
| updated_at | timestamp (text in CSV) | Last update time. Used as the watermark for incremental loads |

## Relationships
- sales.customer_id -> customers.customer_id
- sales.product_id -> products.product_id

## Data quality notes
- coupon_code is legitimately null for about half the rows.
- Dates are stored as text in the source files and converted in Phase 4.
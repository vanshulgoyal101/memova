# Liqo Retail Chain Database Schema

## Overview

**Database**: `liqo_company.db`  
**Domain**: Retail Electronics & Home Appliances  
**Time Period**: FY 2022-23 (April 2022 - March 2023)  
**Geography**: North India (Punjab, Haryana, Himachal Pradesh)  
**Size**: 7.9 MB

### Business Context

Liqo is a retail electronics and home appliances chain operating in North India with 5 store locations. The database contains 37,857 sales transactions covering a complete fiscal year, tracking customer purchases, product inventory, sales performance, and location-wise revenue.

**Key Metrics**:
- **37,857 transactions** across 12 months
- **5 store locations**: Kharar, Chandigarh, Ramgarh, Panchkula, Solan
- **7,914 unique customers** (B2B and B2C)
- **10,768 unique products** across multiple brands
- **147 salespeople**
- **Total Revenue**: ₹60.9 Crores (~$7.3M USD)

---

## Database Schema

### 1. locations

Store locations and their regional information.

```sql
CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_name TEXT NOT NULL UNIQUE,
    state TEXT,
    material_centre TEXT
);
```

**Columns**:
- `location_id`: Unique identifier
- `location_name`: Store location name (Kharar, Chandigarh, etc.)
- `state`: State where store is located
- `material_centre`: Distribution/material center code

**Sample Data**:
```
location_id | location_name | state           | material_centre
1           | Kharar        | Punjab          | MC_KHARAR
2           | Chandigarh    | Chandigarh      | MC_CHD
3           | Ramgarh       | Haryana         | MC_RAMGARH
4           | Panchkula     | Haryana         | MC_PKL
5           | Solan         | Himachal Pradesh| MC_SOLAN
```

---

### 2. customers

Customer information with business type classification.

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    address TEXT,
    state TEXT,
    gst_number TEXT,
    customer_type TEXT -- B2B or B2C
);
```

**Columns**:
- `customer_id`: Unique identifier
- `customer_name`: Customer full name/business name
- `address`: Customer address
- `state`: Customer's state
- `gst_number`: GST registration number (for B2B customers)
- `customer_type`: B2B (Business) or B2C (Consumer)

**Statistics**:
- Total customers: 7,914
- B2B customers: ~18% (with GST numbers)
- B2C customers: ~82% (walk-in retail)

---

### 3. salespeople

Sales representatives managing customer relationships.

```sql
CREATE TABLE salespeople (
    salesperson_id INTEGER PRIMARY KEY AUTOINCREMENT,
    salesperson_name TEXT NOT NULL UNIQUE
);
```

**Columns**:
- `salesperson_id`: Unique identifier
- `salesperson_name`: Sales representative name

**Statistics**:
- Total salespeople: 147
- Not all transactions have assigned salespeople (walk-in sales)

---

### 4. products

Product catalog with detailed categorization.

```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    full_description TEXT,
    item_group TEXT,
    brand TEXT,
    model TEXT,
    source TEXT,
    main_category TEXT,
    sub_category TEXT,
    capacity TEXT,
    type1 TEXT
);
```

**Columns**:
- `product_id`: Unique identifier
- `item_name`: Product name
- `full_description`: Detailed product description
- `item_group`: Product grouping code
- `brand`: Manufacturer brand (Voltas, IFB, Samsung, LG, etc.)
- `model`: Model number
- `source`: Product source/supplier
- `main_category`: Primary category (AC, Refrigerator, LED TV, etc.)
- `sub_category`: Detailed sub-category
- `capacity`: Product capacity (1.5 Ton, 190L, 43 Inch, etc.)
- `type1`: Additional type classification

**Main Categories**:
- **AC** (Air Conditioners)
- **Refrigerator**
- **LED TV**
- **Washing Machine**
- **Accessories**
- **Microwave Oven**
- **Water Heater**
- **Kitchen Appliances**
- **Small Appliances**
- **Others**

**Top Brands**:
- Voltas, LG, Samsung, IFB, Whirlpool, Godrej, Haier, Panasonic, Sony, etc.

---

### 5. sales_transactions

Core transactional data linking all entities.

```sql
CREATE TABLE sales_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    customer_id INTEGER,
    salesperson_id INTEGER,
    product_id INTEGER,
    voucher_number TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    month TEXT,
    fiscal_year TEXT,
    quantity REAL NOT NULL,
    item_amount REAL NOT NULL,
    taxable_amount REAL NOT NULL,
    transaction_type TEXT, -- Cash, Credit, etc.
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (salesperson_id) REFERENCES salespeople(salesperson_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**Columns**:
- `transaction_id`: Unique identifier
- `location_id`: Store location reference
- `customer_id`: Customer reference
- `salesperson_id`: Salesperson reference (nullable)
- `product_id`: Product reference
- `voucher_number`: Invoice/bill number
- `transaction_date`: Transaction date (YYYY-MM-DD)
- `month`: Month name (Apr-2022, May-2022, etc.)
- `fiscal_year`: Fiscal year (2022-23)
- `quantity`: Number of units sold
- `item_amount`: Total amount including tax
- `taxable_amount`: Amount before tax
- `transaction_type`: Payment method (Cash, Credit, UPI, etc.)

**Indexes** (for performance):
- `idx_transactions_date` on transaction_date
- `idx_transactions_location` on location_id
- `idx_transactions_customer` on customer_id
- `idx_transactions_product` on product_id

---

## Sample Queries

### Basic Revenue Queries

**Q1: Total revenue for FY 2022-23**
```sql
SELECT SUM(item_amount) AS total_revenue
FROM sales_transactions
WHERE fiscal_year = '2022-23';
```

**Q2: Revenue by location**
```sql
SELECT 
    l.location_name,
    COUNT(st.transaction_id) AS transaction_count,
    SUM(st.item_amount) AS total_revenue
FROM sales_transactions st
JOIN locations l ON st.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_revenue DESC;
```

**Q3: Monthly revenue trend**
```sql
SELECT 
    month,
    COUNT(*) AS transactions,
    SUM(item_amount) AS revenue,
    AVG(item_amount) AS avg_transaction_value
FROM sales_transactions
GROUP BY month
ORDER BY transaction_date;
```

### Product Analysis

**Q4: Top 10 products by revenue**
```sql
SELECT 
    p.item_name,
    p.brand,
    p.main_category,
    COUNT(st.transaction_id) AS units_sold,
    SUM(st.item_amount) AS total_revenue
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;
```

**Q5: Revenue by product category**
```sql
SELECT 
    p.main_category,
    COUNT(st.transaction_id) AS transactions,
    SUM(st.quantity) AS units_sold,
    SUM(st.item_amount) AS revenue
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
GROUP BY p.main_category
ORDER BY revenue DESC;
```

**Q6: Brand performance**
```sql
SELECT 
    p.brand,
    COUNT(DISTINCT p.product_id) AS product_count,
    COUNT(st.transaction_id) AS transactions,
    SUM(st.item_amount) AS revenue
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
WHERE p.brand IS NOT NULL
GROUP BY p.brand
ORDER BY revenue DESC
LIMIT 15;
```

### Customer Analysis

**Q7: B2B vs B2C comparison**
```sql
SELECT 
    c.customer_type,
    COUNT(DISTINCT st.customer_id) AS unique_customers,
    COUNT(st.transaction_id) AS transactions,
    SUM(st.item_amount) AS revenue,
    AVG(st.item_amount) AS avg_transaction
FROM sales_transactions st
JOIN customers c ON st.customer_id = c.customer_id
GROUP BY c.customer_type;
```

**Q8: Top 10 customers by revenue**
```sql
SELECT 
    c.customer_name,
    c.customer_type,
    c.state,
    COUNT(st.transaction_id) AS purchases,
    SUM(st.item_amount) AS total_spent
FROM sales_transactions st
JOIN customers c ON st.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;
```

**Q9: Customer state distribution**
```sql
SELECT 
    c.state,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(st.transaction_id) AS transactions,
    SUM(st.item_amount) AS revenue
FROM customers c
LEFT JOIN sales_transactions st ON c.customer_id = st.customer_id
GROUP BY c.state
ORDER BY revenue DESC;
```

### Sales Performance

**Q10: Top performing salespeople**
```sql
SELECT 
    sp.salesperson_name,
    COUNT(st.transaction_id) AS transactions,
    SUM(st.item_amount) AS total_sales,
    AVG(st.item_amount) AS avg_deal_size
FROM sales_transactions st
JOIN salespeople sp ON st.salesperson_id = sp.salesperson_id
GROUP BY sp.salesperson_id
ORDER BY total_sales DESC
LIMIT 10;
```

**Q11: Location-wise sales performance**
```sql
SELECT 
    l.location_name,
    l.state,
    COUNT(DISTINCT st.customer_id) AS unique_customers,
    COUNT(st.transaction_id) AS transactions,
    SUM(st.item_amount) AS revenue,
    AVG(st.item_amount) AS avg_transaction
FROM sales_transactions st
JOIN locations l ON st.location_id = l.location_id
GROUP BY l.location_id
ORDER BY revenue DESC;
```

### Advanced Analytics

**Q12: Seasonal trends by product category**
```sql
SELECT 
    p.main_category,
    st.month,
    COUNT(*) AS transactions,
    SUM(st.item_amount) AS revenue
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
WHERE p.main_category IN ('AC', 'Refrigerator', 'LED TV', 'Washing Machine')
GROUP BY p.main_category, st.month
ORDER BY p.main_category, st.transaction_date;
```

**Q13: Product mix by location**
```sql
SELECT 
    l.location_name,
    p.main_category,
    COUNT(*) AS transactions,
    SUM(st.item_amount) AS revenue
FROM sales_transactions st
JOIN locations l ON st.location_id = l.location_id
JOIN products p ON st.product_id = p.product_id
GROUP BY l.location_name, p.main_category
ORDER BY l.location_name, revenue DESC;
```

**Q14: Average transaction value trends**
```sql
SELECT 
    month,
    COUNT(*) AS transactions,
    SUM(item_amount) AS total_revenue,
    AVG(item_amount) AS avg_transaction,
    MIN(item_amount) AS min_transaction,
    MAX(item_amount) AS max_transaction
FROM sales_transactions
GROUP BY month
ORDER BY transaction_date;
```

---

## Business Insights

### Revenue Distribution
- **Peak months**: Festival seasons (Oct-Nov, Feb-Mar)
- **Top categories**: AC (~25%), LED TV (~20%), Refrigerator (~18%)
- **Location dominance**: Chandigarh and Kharar contribute ~60% of revenue

### Customer Behavior
- **B2B transactions**: Higher average value (₹45K vs ₹15K for B2C)
- **Repeat customers**: ~35% make multiple purchases
- **Peak buying days**: Weekends and festival periods

### Product Trends
- **Brand preferences**: Samsung, LG dominate in electronics
- **Capacity preferences**: 1.5 Ton AC, 190L Fridge most popular
- **Accessories**: High volume, lower margin

---

## Query Patterns

### What Works Well
✅ Revenue analysis by time, location, category  
✅ Product performance and ranking queries  
✅ Customer segmentation (B2B/B2C)  
✅ Salesperson performance tracking  
✅ Trend analysis over months  

### Domain-Specific Keywords
- **Sales**: revenue, transactions, purchases
- **Products**: items, brands, categories, models
- **Locations**: stores, branches, outlets
- **Customers**: buyers, clients, B2B, B2C
- **Salespeople**: sales rep, sales person

### Example Questions
- "What is the total revenue for FY 2022-23?"
- "Show me top 10 products by sales"
- "Which location has the highest revenue?"
- "Compare B2B vs B2C sales"
- "Show monthly revenue trends"
- "Which brands are most popular?"
- "Top performing salespeople by revenue"
- "Show me sales by product category"

---

## Schema Generation

**Source**: `Raw_Data_FY_2022-23.xlsx` (single sheet, 26 columns)  
**Generator**: `src/data/liqo_generators.py`  
**Command**: `python -m src.data.liqo_generators`

**Normalization Process**:
1. Extract unique locations, customers, products, salespeople
2. Create relational structure with foreign keys
3. Deduplicate based on business logic (customer name, product name)
4. Add indexes for query performance
5. Maintain referential integrity

---

## Data Quality

**Completeness**:
- ✅ All transactions have dates, amounts, voucher numbers
- ⚠️ ~46% transactions have null salesperson (walk-in sales)
- ⚠️ ~11% customers missing address
- ⚠️ ~48% products missing brand info

**Consistency**:
- ✅ All dates within FY 2022-23 range
- ✅ All amounts are positive
- ✅ Foreign key relationships maintained

**Coverage**:
- 361 unique transaction dates (nearly complete year)
- 12 months fully represented
- All 5 locations have transactions

---

## Related Documentation

- [System Overview](../02-architecture/system-overview.md) - How queries work
- [API Endpoints](../05-api/endpoints.md) - How to query this database
- [Natural Language Queries](../03-features/natural-language.md) - AI-powered querying

---

**Last Updated**: 2025-11-07  
**Database Version**: 1.0  
**Schema Version**: 1.0

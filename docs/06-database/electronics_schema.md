# 📊 Electronics Appliance Company - Database Schema

**Generated:** 2025-11-01 12:55:31

**Database:** /Volumes/Extreme SSD/code/sql schema/data/database/electronics_company.db

**Total Tables:** 12

---

## 📑 Table of Contents

1. [Customer Service Tickets](#customer_service_tickets)
2. [Customers](#customers)
3. [Employees](#employees)
4. [Financial Transactions](#financial_transactions)
5. [Inventory](#inventory)
6. [Marketing Campaigns](#marketing_campaigns)
7. [Payroll](#payroll)
8. [Products](#products)
9. [Sales Orders](#sales_orders)
10. [Shipments](#shipments)
11. [Suppliers](#suppliers)
12. [Warranties](#warranties)

---

## 🎯 Database Overview

This database contains comprehensive data for an electronics appliance selling company, including:

- **HR & Payroll**: Employee management and compensation data
- **Sales & Orders**: Customer orders and sales transactions
- **Inventory**: Product stock and warehouse management
- **Finance**: Financial transactions and accounting
- **Customer Service**: Support tickets and warranty claims
- **Marketing**: Campaign tracking and analytics
- **Logistics**: Shipping and delivery information

---

## 🔗 Key Relationships

```
employees ──→ sales_orders (employee_id)
employees ──→ payroll (employee_id)
employees ──→ customer_service_tickets (assigned_employee_id)

customers ──→ sales_orders (customer_id)
customers ──→ customer_service_tickets (customer_id)
customers ──→ warranties (customer_id)

products ──→ sales_orders (product_id)
products ──→ inventory (product_id)
products ──→ customer_service_tickets (product_id)
products ──→ warranties (product_id)
products ──→ suppliers (supplier_id)

sales_orders ──→ shipments (order_id)
```

---

## 📋 Detailed Table Schemas

### <a id='customer_service_tickets'></a>Customer Service Tickets

**Description:** Customer support tickets tracking issues, resolutions, and satisfaction.

**Row Count:** 180

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `ticket_id` | TEXT | Yes | NULL |  | Unique identifier |
| `customer_id` | TEXT | Yes | NULL |  | Customer unique identifier |
| `product_id` | TEXT | Yes | NULL |  | Product unique identifier |
| `assigned_employee_id` | TEXT | Yes | NULL |  | Unique identifier |
| `ticket_type` | TEXT | Yes | NULL |  | Ticket Type |
| `priority` | TEXT | Yes | NULL |  | Priority |
| `status` | TEXT | Yes | NULL |  | Current status |
| `created_date` | DATETIME | Yes | NULL |  | Record creation date |
| `resolved_date` | DATETIME | Yes | NULL |  | Date |
| `subject` | TEXT | Yes | NULL |  | Subject |
| `description` | TEXT | Yes | NULL |  | Description |
| `resolution_notes` | TEXT | Yes | NULL |  | Resolution Notes |
| `satisfaction_rating` | FLOAT | Yes | NULL |  | Satisfaction Rating |
| `channel` | TEXT | Yes | NULL |  | Channel |

**Sample Data:**
```
ticket_id | customer_id | product_id | assigned_employee_id | ticket_type
-----------------------------------------------------------------------------------
TKT000001 | CUS00040 | PRD00043 | EMP00146 | Delivery Issue
TKT000002 | CUS00049 | PRD00043 | EMP00146 | Return Request
TKT000003 | CUS00177 | PRD00004 | EMP00048 | Complaint

... and 9 more columns
```

---

### <a id='customers'></a>Customers

**Description:** Customer database with contact information, registration details, and loyalty data.

**Row Count:** 200

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `customer_id` | TEXT | Yes | NULL |  | Customer unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `customer_type` | TEXT | Yes | NULL |  | Customer Type |
| `address` | TEXT | Yes | NULL |  | Street address |
| `city` | TEXT | Yes | NULL |  | City name |
| `state` | TEXT | Yes | NULL |  | State code |
| `zip_code` | BIGINT | Yes | NULL |  | ZIP/Postal code |
| `registration_date` | DATETIME | Yes | NULL |  | Date |
| `loyalty_points` | BIGINT | Yes | NULL |  | Loyalty Points |
| `credit_limit` | BIGINT | Yes | NULL |  | Credit Limit |
| `preferred_contact` | TEXT | Yes | NULL |  | Preferred Contact |

**Sample Data:**
```
customer_id | first_name | last_name | email | phone
--------------------------------------------------------------
CUS00001 | Timothy | Mack | brianna91@example.co | (647)531-4986
CUS00002 | Ronald | Richards | melissa69@example.co | +1-946-636-8872x588
CUS00003 | Brett | Price | brockmadeline@exampl | +1-661-214-3519x066

... and 9 more columns
```

---

### <a id='employees'></a>Employees

**Description:** Employee records including personal information, department, position, and compensation details.

**Row Count:** 150

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `department` | TEXT | Yes | NULL |  | Department |
| `position` | TEXT | Yes | NULL |  | Position |
| `hire_date` | DATETIME | Yes | NULL |  | Date |
| `salary` | BIGINT | Yes | NULL |  | Salary |
| `manager_id` | TEXT | Yes | NULL |  | Unique identifier |
| `status` | TEXT | Yes | NULL |  | Current status |
| `city` | TEXT | Yes | NULL |  | City name |
| `state` | TEXT | Yes | NULL |  | State code |
| `birth_date` | DATETIME | Yes | NULL |  | Date |

**Sample Data:**
```
employee_id | first_name | last_name | email | phone
--------------------------------------------------------------
EMP00001 | Danielle | Johnson | john21@example.net | 001-581-896-0013x389
EMP00002 | Helen | Peterson | jasongallagher@examp | 361-855-9407
EMP00003 | Chad | Stanley | tracie31@example.com | 575-425-5341x928

... and 9 more columns
```

---

### <a id='financial_transactions'></a>Financial Transactions

**Description:** Financial records including revenue, expenses, and various business transactions.

**Row Count:** 250

**Column Count:** 13

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `transaction_id` | TEXT | Yes | NULL |  | Unique identifier |
| `transaction_date` | DATETIME | Yes | NULL |  | Date |
| `transaction_type` | TEXT | Yes | NULL |  | Transaction Type |
| `category` | TEXT | Yes | NULL |  | Category |
| `amount` | BIGINT | Yes | NULL |  | Amount |
| `account_number` | TEXT | Yes | NULL |  | Account Number |
| `reference_number` | TEXT | Yes | NULL |  | Reference Number |
| `description` | TEXT | Yes | NULL |  | Description |
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `vendor_customer` | TEXT | Yes | NULL |  | Vendor Customer |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |
| `status` | TEXT | Yes | NULL |  | Current status |
| `fiscal_year` | BIGINT | Yes | NULL |  | Fiscal Year |

**Sample Data:**
```
transaction_id | transaction_date | transaction_type | category | amount
----------------------------------------------------------------------------------
TXN000001 | 2025-06-14 00:00:00. | Refund | Salaries | -38115
TXN000002 | 2024-01-18 00:00:00. | Revenue | Taxes | 46050
TXN000003 | 2024-07-16 00:00:00. | Salary | Taxes | -31509

... and 8 more columns
```

---

### <a id='inventory'></a>Inventory

**Description:** Stock management data for products across different warehouse locations.

**Row Count:** 120

**Column Count:** 13

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `inventory_id` | TEXT | Yes | NULL |  | Unique identifier |
| `product_id` | TEXT | Yes | NULL |  | Product unique identifier |
| `warehouse_location` | TEXT | Yes | NULL |  | Warehouse Location |
| `quantity_in_stock` | BIGINT | Yes | NULL |  | Quantity |
| `reorder_level` | BIGINT | Yes | NULL |  | Reorder Level |
| `reorder_quantity` | BIGINT | Yes | NULL |  | Quantity |
| `last_restock_date` | DATETIME | Yes | NULL |  | Date |
| `expiry_date` | DATETIME | Yes | NULL |  | Date |
| `bin_location` | TEXT | Yes | NULL |  | Bin Location |
| `reserved_quantity` | BIGINT | Yes | NULL |  | Quantity |
| `damaged_quantity` | BIGINT | Yes | NULL |  | Quantity |
| `unit_cost` | BIGINT | Yes | NULL |  | Unit Cost |
| `total_value` | BIGINT | Yes | NULL |  | Total Value |

**Sample Data:**
```
inventory_id | product_id | warehouse_location | quantity_in_stock | reorder_level
--------------------------------------------------------------------------------------------
INV000001 | PRD00001 | Warehouse B | 437 | 20
INV000002 | PRD00002 | Warehouse A | 32 | 49
INV000003 | PRD00003 | Warehouse C | 316 | 24

... and 8 more columns
```

---

### <a id='marketing_campaigns'></a>Marketing Campaigns

**Description:** Marketing campaign data with budget, performance metrics, and ROI analysis.

**Row Count:** 40

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `campaign_id` | TEXT | Yes | NULL |  | Unique identifier |
| `campaign_name` | TEXT | Yes | NULL |  | Name |
| `channel` | TEXT | Yes | NULL |  | Channel |
| `start_date` | DATETIME | Yes | NULL |  | Date |
| `end_date` | DATETIME | Yes | NULL |  | Date |
| `budget` | BIGINT | Yes | NULL |  | Budget |
| `actual_spend` | BIGINT | Yes | NULL |  | Actual Spend |
| `impressions` | BIGINT | Yes | NULL |  | Impressions |
| `clicks` | BIGINT | Yes | NULL |  | Clicks |
| `conversions` | BIGINT | Yes | NULL |  | Conversions |
| `revenue_generated` | BIGINT | Yes | NULL |  | Revenue Generated |
| `roi` | FLOAT | Yes | NULL |  | Roi |
| `target_audience` | TEXT | Yes | NULL |  | Target Audience |
| `status` | TEXT | Yes | NULL |  | Current status |

**Sample Data:**
```
campaign_id | campaign_name | channel | start_date | end_date
-----------------------------------------------------------------------
CMP00001 | Operative contextual | TV | 2025-04-06 00:00:00. | 2025-10-31 00:00:00.
CMP00002 | Implemented hybrid a | Online Ads | 2025-09-24 00:00:00. | 2025-10-31 00:00:00.
CMP00003 | Streamlined context- | Social Media | 2024-02-12 00:00:00. | 2025-10-31 00:00:00.

... and 9 more columns
```

---

### <a id='payroll'></a>Payroll

**Description:** Employee payroll information including salary, taxes, deductions, and payment details.

**Row Count:** 150

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `payroll_id` | TEXT | Yes | NULL |  | Unique identifier |
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `pay_period_start` | DATETIME | Yes | NULL |  | Pay Period Start |
| `pay_period_end` | DATETIME | Yes | NULL |  | Pay Period End |
| `base_salary` | BIGINT | Yes | NULL |  | Base Salary |
| `overtime_pay` | BIGINT | Yes | NULL |  | Overtime Pay |
| `bonus` | BIGINT | Yes | NULL |  | Bonus |
| `gross_pay` | BIGINT | Yes | NULL |  | Gross Pay |
| `federal_tax` | FLOAT | Yes | NULL |  | Federal Tax |
| `state_tax` | FLOAT | Yes | NULL |  | State code |
| `health_insurance` | BIGINT | Yes | NULL |  | Health Insurance |
| `retirement_contribution` | FLOAT | Yes | NULL |  | Retirement Contribution |
| `net_pay` | FLOAT | Yes | NULL |  | Net Pay |
| `payment_date` | DATETIME | Yes | NULL |  | Date |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |

**Sample Data:**
```
payroll_id | employee_id | pay_period_start | pay_period_end | base_salary
------------------------------------------------------------------------------------
PAY000001 | EMP00001 | 2025-10-04 00:00:00. | 2025-01-02 00:00:00. | 5473
PAY000002 | EMP00002 | 2025-07-07 00:00:00. | 2025-06-03 00:00:00. | 9869
PAY000003 | EMP00003 | 2025-03-18 00:00:00. | 2025-01-14 00:00:00. | 8638

... and 10 more columns
```

---

### <a id='products'></a>Products

**Description:** Product catalog with specifications, pricing, warranty, and supplier information.

**Row Count:** 120

**Column Count:** 13

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `product_id` | TEXT | Yes | NULL |  | Product unique identifier |
| `product_name` | TEXT | Yes | NULL |  | Name |
| `category` | TEXT | Yes | NULL |  | Category |
| `brand` | TEXT | Yes | NULL |  | Brand |
| `model_number` | TEXT | Yes | NULL |  | Model Number |
| `cost_price` | BIGINT | Yes | NULL |  | Price |
| `selling_price` | BIGINT | Yes | NULL |  | Price |
| `warranty_months` | BIGINT | Yes | NULL |  | Warranty Months |
| `weight_kg` | FLOAT | Yes | NULL |  | Weight Kg |
| `energy_rating` | TEXT | Yes | NULL |  | Energy Rating |
| `release_date` | DATETIME | Yes | NULL |  | Date |
| `supplier_id` | TEXT | Yes | NULL |  | Unique identifier |
| `status` | TEXT | Yes | NULL |  | Current status |

**Sample Data:**
```
product_id | product_name | category | brand | model_number
---------------------------------------------------------------------
PRD00001 | Bosch Refrigerators  | Water Heaters | LG | Im600Ux
PRD00002 | Whirlpool Kitchen Ap | Audio Systems | Philips | bR583aO
PRD00003 | LG Microwave Ovens B | Televisions | Haier | ig354yG

... and 8 more columns
```

---

### <a id='sales_orders'></a>Sales Orders

**Description:** Sales transaction records including order details, pricing, and delivery information.

**Row Count:** 300

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `order_id` | TEXT | Yes | NULL |  | Order unique identifier |
| `customer_id` | TEXT | Yes | NULL |  | Customer unique identifier |
| `product_id` | TEXT | Yes | NULL |  | Product unique identifier |
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `order_date` | DATETIME | Yes | NULL |  | Date |
| `delivery_date` | DATETIME | Yes | NULL |  | Date |
| `quantity` | BIGINT | Yes | NULL |  | Quantity |
| `unit_price` | BIGINT | Yes | NULL |  | Price |
| `subtotal` | BIGINT | Yes | NULL |  | Subtotal |
| `tax_amount` | FLOAT | Yes | NULL |  | Tax Amount |
| `discount_amount` | FLOAT | Yes | NULL |  | Discount Amount |
| `total_amount` | FLOAT | Yes | NULL |  | Total amount |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |
| `status` | TEXT | Yes | NULL |  | Current status |
| `shipping_address` | TEXT | Yes | NULL |  | Street address |

**Sample Data:**
```
order_id | customer_id | product_id | employee_id | order_date
------------------------------------------------------------------------
ORD000001 | CUS00138 | PRD00024 | EMP00094 | 2024-12-21 00:00:00.
ORD000002 | CUS00136 | PRD00082 | EMP00081 | 2025-10-06 00:00:00.
ORD000003 | CUS00091 | PRD00109 | EMP00118 | 2025-07-27 00:00:00.

... and 10 more columns
```

---

### <a id='shipments'></a>Shipments

**Description:** Shipment tracking information including carrier details and delivery status.

**Row Count:** 280

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `shipment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `order_id` | TEXT | Yes | NULL |  | Order unique identifier |
| `carrier` | TEXT | Yes | NULL |  | Carrier |
| `tracking_number` | TEXT | Yes | NULL |  | Tracking Number |
| `ship_date` | DATETIME | Yes | NULL |  | Date |
| `estimated_delivery` | DATETIME | Yes | NULL |  | Estimated Delivery |
| `actual_delivery` | DATETIME | Yes | NULL |  | Actual Delivery |
| `origin_city` | TEXT | Yes | NULL |  | City name |
| `origin_state` | TEXT | Yes | NULL |  | State code |
| `destination_city` | TEXT | Yes | NULL |  | City name |
| `destination_state` | TEXT | Yes | NULL |  | State code |
| `weight_kg` | FLOAT | Yes | NULL |  | Weight Kg |
| `shipping_cost` | FLOAT | Yes | NULL |  | Shipping Cost |
| `status` | TEXT | Yes | NULL |  | Current status |

**Sample Data:**
```
shipment_id | order_id | carrier | tracking_number | ship_date
------------------------------------------------------------------------
SHIP000001 | ORD000036 | UPS | nu9640101460193 | 2025-07-03 00:00:00.
SHIP000002 | ORD000220 | DHL | sd9316426633161 | 2024-11-18 00:00:00.
SHIP000003 | ORD000005 | Local Courier | eM9457405199508 | 2025-06-07 00:00:00.

... and 9 more columns
```

---

### <a id='suppliers'></a>Suppliers

**Description:** Supplier information including contact details and business terms.

**Row Count:** 30

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `supplier_id` | TEXT | Yes | NULL |  | Unique identifier |
| `supplier_name` | TEXT | Yes | NULL |  | Name |
| `contact_person` | TEXT | Yes | NULL |  | Contact Person |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `address` | TEXT | Yes | NULL |  | Street address |
| `city` | TEXT | Yes | NULL |  | City name |
| `state` | TEXT | Yes | NULL |  | State code |
| `country` | TEXT | Yes | NULL |  | Country |
| `zip_code` | BIGINT | Yes | NULL |  | ZIP/Postal code |
| `payment_terms` | TEXT | Yes | NULL |  | Payment Terms |
| `rating` | FLOAT | Yes | NULL |  | Rating |
| `total_orders` | BIGINT | Yes | NULL |  | Total Orders |
| `active_since` | DATETIME | Yes | NULL |  | Active Since |

**Sample Data:**
```
supplier_id | supplier_name | contact_person | email | phone
----------------------------------------------------------------------
SUP00001 | Shaffer Inc | Kyle Fox | stephenscatherine@al | 932.765.3060x1198
SUP00002 | Glass, Sanchez and B | Michael Baker | mackenzie91@velez.co | (659)352-0149x1189
SUP00003 | Rogers-Barnes | Timothy Dominguez | david86@williams.com | 476.866.0811

... and 9 more columns
```

---

### <a id='warranties'></a>Warranties

**Description:** Product warranty registrations and claim tracking information.

**Row Count:** 250

**Column Count:** 13

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `warranty_id` | TEXT | Yes | NULL |  | Unique identifier |
| `product_id` | TEXT | Yes | NULL |  | Product unique identifier |
| `customer_id` | TEXT | Yes | NULL |  | Customer unique identifier |
| `purchase_date` | DATETIME | Yes | NULL |  | Date |
| `warranty_start_date` | DATETIME | Yes | NULL |  | Date |
| `warranty_end_date` | DATETIME | Yes | NULL |  | Date |
| `warranty_type` | TEXT | Yes | NULL |  | Warranty Type |
| `coverage_amount` | BIGINT | Yes | NULL |  | Coverage Amount |
| `registration_date` | DATETIME | Yes | NULL |  | Date |
| `claim_count` | BIGINT | Yes | NULL |  | Claim Count |
| `status` | TEXT | Yes | NULL |  | Current status |
| `serial_number` | TEXT | Yes | NULL |  | Serial Number |
| `notes` | TEXT | Yes | NULL |  | Notes |

**Sample Data:**
```
warranty_id | product_id | customer_id | purchase_date | warranty_start_date
--------------------------------------------------------------------------------------
WAR000001 | PRD00110 | CUS00041 | 2024-06-18 00:00:00. | 2024-06-18 00:00:00.
WAR000002 | PRD00030 | CUS00068 | 2025-05-24 00:00:00. | 2025-05-24 00:00:00.
WAR000003 | PRD00107 | CUS00191 | 2023-06-26 00:00:00. | 2023-06-26 00:00:00.

... and 8 more columns
```

---

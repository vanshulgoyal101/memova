-- Electronics Appliance Company Database Schema
-- Generated: 2025-11-01 12:55:31
-- Total Tables: 12


-- Table: customer_service_tickets
CREATE TABLE customer_service_tickets (
	ticket_id TEXT, 
	customer_id TEXT, 
	product_id TEXT, 
	assigned_employee_id TEXT, 
	ticket_type TEXT, 
	priority TEXT, 
	status TEXT, 
	created_date DATETIME, 
	resolved_date DATETIME, 
	subject TEXT, 
	description TEXT, 
	resolution_notes TEXT, 
	satisfaction_rating FLOAT, 
	channel TEXT
);


-- Table: customers
CREATE TABLE customers (
	customer_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	email TEXT, 
	phone TEXT, 
	customer_type TEXT, 
	address TEXT, 
	city TEXT, 
	state TEXT, 
	zip_code BIGINT, 
	registration_date DATETIME, 
	loyalty_points BIGINT, 
	credit_limit BIGINT, 
	preferred_contact TEXT
);


-- Table: employees
CREATE TABLE employees (
	employee_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	email TEXT, 
	phone TEXT, 
	department TEXT, 
	position TEXT, 
	hire_date DATETIME, 
	salary BIGINT, 
	manager_id TEXT, 
	status TEXT, 
	city TEXT, 
	state TEXT, 
	birth_date DATETIME
);


-- Table: financial_transactions
CREATE TABLE financial_transactions (
	transaction_id TEXT, 
	transaction_date DATETIME, 
	transaction_type TEXT, 
	category TEXT, 
	amount BIGINT, 
	account_number TEXT, 
	reference_number TEXT, 
	description TEXT, 
	employee_id TEXT, 
	vendor_customer TEXT, 
	payment_method TEXT, 
	status TEXT, 
	fiscal_year BIGINT
);


-- Table: inventory
CREATE TABLE inventory (
	inventory_id TEXT, 
	product_id TEXT, 
	warehouse_location TEXT, 
	quantity_in_stock BIGINT, 
	reorder_level BIGINT, 
	reorder_quantity BIGINT, 
	last_restock_date DATETIME, 
	expiry_date DATETIME, 
	bin_location TEXT, 
	reserved_quantity BIGINT, 
	damaged_quantity BIGINT, 
	unit_cost BIGINT, 
	total_value BIGINT
);


-- Table: marketing_campaigns
CREATE TABLE marketing_campaigns (
	campaign_id TEXT, 
	campaign_name TEXT, 
	channel TEXT, 
	start_date DATETIME, 
	end_date DATETIME, 
	budget BIGINT, 
	actual_spend BIGINT, 
	impressions BIGINT, 
	clicks BIGINT, 
	conversions BIGINT, 
	revenue_generated BIGINT, 
	roi FLOAT, 
	target_audience TEXT, 
	status TEXT
);


-- Table: payroll
CREATE TABLE payroll (
	payroll_id TEXT, 
	employee_id TEXT, 
	pay_period_start DATETIME, 
	pay_period_end DATETIME, 
	base_salary BIGINT, 
	overtime_pay BIGINT, 
	bonus BIGINT, 
	gross_pay BIGINT, 
	federal_tax FLOAT, 
	state_tax FLOAT, 
	health_insurance BIGINT, 
	retirement_contribution FLOAT, 
	net_pay FLOAT, 
	payment_date DATETIME, 
	payment_method TEXT
);


-- Table: products
CREATE TABLE products (
	product_id TEXT, 
	product_name TEXT, 
	category TEXT, 
	brand TEXT, 
	model_number TEXT, 
	cost_price BIGINT, 
	selling_price BIGINT, 
	warranty_months BIGINT, 
	weight_kg FLOAT, 
	energy_rating TEXT, 
	release_date DATETIME, 
	supplier_id TEXT, 
	status TEXT
);


-- Table: sales_orders
CREATE TABLE sales_orders (
	order_id TEXT, 
	customer_id TEXT, 
	product_id TEXT, 
	employee_id TEXT, 
	order_date DATETIME, 
	delivery_date DATETIME, 
	quantity BIGINT, 
	unit_price BIGINT, 
	subtotal BIGINT, 
	tax_amount FLOAT, 
	discount_amount FLOAT, 
	total_amount FLOAT, 
	payment_method TEXT, 
	status TEXT, 
	shipping_address TEXT
);


-- Table: shipments
CREATE TABLE shipments (
	shipment_id TEXT, 
	order_id TEXT, 
	carrier TEXT, 
	tracking_number TEXT, 
	ship_date DATETIME, 
	estimated_delivery DATETIME, 
	actual_delivery DATETIME, 
	origin_city TEXT, 
	origin_state TEXT, 
	destination_city TEXT, 
	destination_state TEXT, 
	weight_kg FLOAT, 
	shipping_cost FLOAT, 
	status TEXT
);


-- Table: suppliers
CREATE TABLE suppliers (
	supplier_id TEXT, 
	supplier_name TEXT, 
	contact_person TEXT, 
	email TEXT, 
	phone TEXT, 
	address TEXT, 
	city TEXT, 
	state TEXT, 
	country TEXT, 
	zip_code BIGINT, 
	payment_terms TEXT, 
	rating FLOAT, 
	total_orders BIGINT, 
	active_since DATETIME
);


-- Table: warranties
CREATE TABLE warranties (
	warranty_id TEXT, 
	product_id TEXT, 
	customer_id TEXT, 
	purchase_date DATETIME, 
	warranty_start_date DATETIME, 
	warranty_end_date DATETIME, 
	warranty_type TEXT, 
	coverage_amount BIGINT, 
	registration_date DATETIME, 
	claim_count BIGINT, 
	status TEXT, 
	serial_number TEXT, 
	notes TEXT
);


"""
Excel to SQL Database Generator for Electronics Appliance Company
Generates realistic HR, Sales, Finance, Inventory, and other business data
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

from src.utils.config import Config

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Output directory for Excel files - use config
config = Config()
OUTPUT_DIR = config.EXCEL_OUTPUT_DIR


def generate_employees(num_rows=150):
    """Generate employee data for HR department"""
    departments = ['Sales', 'Finance', 'HR', 'IT', 'Operations', 'Marketing', 'Customer Service', 'Logistics']
    positions = ['Manager', 'Senior Associate', 'Associate', 'Junior Associate', 'Intern', 'Director', 'VP']
    
    data = []
    for i in range(num_rows):
        data.append({
            'employee_id': f'EMP{str(i+1).zfill(5)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'department': random.choice(departments),
            'position': random.choice(positions),
            'hire_date': fake.date_between(start_date='-10y', end_date='today'),
            'salary': random.randint(35000, 150000),
            'manager_id': f'EMP{str(random.randint(1, max(1, i))).zfill(5)}' if i > 0 else None,
            'status': random.choice(['Active', 'Active', 'Active', 'On Leave', 'Active']),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'birth_date': fake.date_of_birth(minimum_age=22, maximum_age=65)
        })
    
    return pd.DataFrame(data)


def generate_products(num_rows=120):
    """Generate product catalog"""
    categories = ['Refrigerators', 'Washing Machines', 'Air Conditioners', 'Televisions', 
                  'Microwave Ovens', 'Dishwashers', 'Vacuum Cleaners', 'Water Heaters',
                  'Kitchen Appliances', 'Audio Systems']
    brands = ['Samsung', 'LG', 'Whirlpool', 'Sony', 'Panasonic', 'Bosch', 'GE', 'Haier', 'Philips', 'Electrolux']
    
    data = []
    for i in range(num_rows):
        cost = random.randint(100, 3000)
        data.append({
            'product_id': f'PRD{str(i+1).zfill(5)}',
            'product_name': f'{random.choice(brands)} {random.choice(categories)} {random.choice(["Pro", "Plus", "Elite", "Basic", "Smart"])}',
            'category': random.choice(categories),
            'brand': random.choice(brands),
            'model_number': fake.bothify(text='??###??'),
            'cost_price': cost,
            'selling_price': int(cost * random.uniform(1.3, 2.5)),
            'warranty_months': random.choice([6, 12, 24, 36, 60]),
            'weight_kg': round(random.uniform(5, 150), 2),
            'energy_rating': random.choice(['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']),
            'release_date': fake.date_between(start_date='-5y', end_date='today'),
            'supplier_id': f'SUP{str(random.randint(1, 30)).zfill(5)}',
            'status': random.choice(['Active', 'Active', 'Active', 'Discontinued'])
        })
    
    return pd.DataFrame(data)


def generate_customers(num_rows=200):
    """Generate customer data"""
    customer_types = ['Individual', 'Business', 'Government', 'Wholesale']
    
    data = []
    for i in range(num_rows):
        data.append({
            'customer_id': f'CUS{str(i+1).zfill(5)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'customer_type': random.choice(customer_types),
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'registration_date': fake.date_between(start_date='-3y', end_date='today'),
            'loyalty_points': random.randint(0, 5000),
            'credit_limit': random.choice([5000, 10000, 25000, 50000, 100000]),
            'preferred_contact': random.choice(['Email', 'Phone', 'SMS'])
        })
    
    return pd.DataFrame(data)


def generate_sales_orders(num_rows=300):
    """Generate sales orders"""
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer', 'Check', 'Digital Wallet']
    statuses = ['Completed', 'Completed', 'Completed', 'Pending', 'Cancelled', 'Processing']
    
    data = []
    for i in range(num_rows):
        order_date = fake.date_between(start_date='-2y', end_date='today')
        quantity = random.randint(1, 10)
        unit_price = random.randint(200, 5000)
        subtotal = quantity * unit_price
        tax = subtotal * 0.08
        discount = subtotal * random.choice([0, 0, 0.05, 0.10, 0.15])
        
        data.append({
            'order_id': f'ORD{str(i+1).zfill(6)}',
            'customer_id': f'CUS{str(random.randint(1, 200)).zfill(5)}',
            'product_id': f'PRD{str(random.randint(1, 120)).zfill(5)}',
            'employee_id': f'EMP{str(random.randint(1, 150)).zfill(5)}',
            'order_date': order_date,
            'delivery_date': order_date + timedelta(days=random.randint(1, 14)),
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal,
            'tax_amount': round(tax, 2),
            'discount_amount': round(discount, 2),
            'total_amount': round(subtotal + tax - discount, 2),
            'payment_method': random.choice(payment_methods),
            'status': random.choice(statuses),
            'shipping_address': fake.address().replace('\n', ', ')
        })
    
    return pd.DataFrame(data)


def generate_inventory(num_rows=120):
    """Generate inventory data"""
    warehouses = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Warehouse D', 'Retail Store 1', 'Retail Store 2']
    
    data = []
    for i in range(num_rows):
        data.append({
            'inventory_id': f'INV{str(i+1).zfill(6)}',
            'product_id': f'PRD{str(i+1).zfill(5)}',
            'warehouse_location': random.choice(warehouses),
            'quantity_in_stock': random.randint(0, 500),
            'reorder_level': random.randint(20, 50),
            'reorder_quantity': random.randint(50, 200),
            'last_restock_date': fake.date_between(start_date='-6m', end_date='today'),
            'expiry_date': fake.date_between(start_date='today', end_date='+5y') if random.random() > 0.7 else None,
            'bin_location': f'{random.choice(["A", "B", "C", "D"])}-{random.randint(1, 20)}-{random.randint(1, 10)}',
            'reserved_quantity': random.randint(0, 50),
            'damaged_quantity': random.randint(0, 10),
            'unit_cost': random.randint(100, 3000),
            'total_value': 0  # Will calculate
        })
    
    df = pd.DataFrame(data)
    df['total_value'] = df['quantity_in_stock'] * df['unit_cost']
    return df


def generate_suppliers(num_rows=30):
    """Generate supplier data"""
    data = []
    for i in range(num_rows):
        data.append({
            'supplier_id': f'SUP{str(i+1).zfill(5)}',
            'supplier_name': fake.company(),
            'contact_person': fake.name(),
            'email': fake.company_email(),
            'phone': fake.phone_number(),
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'country': 'USA',
            'zip_code': fake.zipcode(),
            'payment_terms': random.choice(['Net 30', 'Net 60', 'Net 90', 'COD', 'Prepaid']),
            'rating': round(random.uniform(3.0, 5.0), 1),
            'total_orders': random.randint(10, 500),
            'active_since': fake.date_between(start_date='-10y', end_date='-1y')
        })
    
    return pd.DataFrame(data)


def generate_financial_transactions(num_rows=250):
    """Generate financial transactions"""
    transaction_types = ['Revenue', 'Expense', 'Asset Purchase', 'Refund', 'Payment', 'Salary', 'Tax']
    categories = ['Sales Revenue', 'Operating Expense', 'Marketing', 'Utilities', 'Rent', 
                  'Salaries', 'Equipment', 'Supplies', 'Services', 'Taxes']
    
    data = []
    for i in range(num_rows):
        trans_type = random.choice(transaction_types)
        amount = random.randint(500, 50000)
        
        data.append({
            'transaction_id': f'TXN{str(i+1).zfill(6)}',
            'transaction_date': fake.date_between(start_date='-2y', end_date='today'),
            'transaction_type': trans_type,
            'category': random.choice(categories),
            'amount': amount if trans_type == 'Revenue' else -amount,
            'account_number': fake.bban(),
            'reference_number': fake.bothify(text='REF-########'),
            'description': fake.sentence(nb_words=6),
            'employee_id': f'EMP{str(random.randint(1, 150)).zfill(5)}',
            'vendor_customer': fake.company() if random.random() > 0.5 else None,
            'payment_method': random.choice(['Bank Transfer', 'Check', 'Credit Card', 'Cash', 'ACH']),
            'status': random.choice(['Completed', 'Completed', 'Pending', 'Completed']),
            'fiscal_year': random.choice([2023, 2024, 2025])
        })
    
    return pd.DataFrame(data)


def generate_payroll(num_rows=150):
    """Generate payroll data"""
    data = []
    for i in range(num_rows):
        base_salary = random.randint(3000, 12000)
        overtime = random.randint(0, 2000)
        bonus = random.randint(0, 5000) if random.random() > 0.7 else 0
        gross_pay = base_salary + overtime + bonus
        tax = gross_pay * 0.22
        insurance = random.randint(200, 800)
        retirement = gross_pay * 0.06
        
        data.append({
            'payroll_id': f'PAY{str(i+1).zfill(6)}',
            'employee_id': f'EMP{str(i+1).zfill(5)}',
            'pay_period_start': fake.date_between(start_date='-1y', end_date='today'),
            'pay_period_end': fake.date_between(start_date='-1y', end_date='today'),
            'base_salary': base_salary,
            'overtime_pay': overtime,
            'bonus': bonus,
            'gross_pay': gross_pay,
            'federal_tax': round(tax * 0.7, 2),
            'state_tax': round(tax * 0.3, 2),
            'health_insurance': insurance,
            'retirement_contribution': round(retirement, 2),
            'net_pay': round(gross_pay - tax - insurance - retirement, 2),
            'payment_date': fake.date_between(start_date='-1y', end_date='today'),
            'payment_method': random.choice(['Direct Deposit', 'Check'])
        })
    
    return pd.DataFrame(data)


def generate_customer_service(num_rows=180):
    """Generate customer service tickets"""
    ticket_types = ['Product Inquiry', 'Complaint', 'Warranty Claim', 'Return Request', 
                    'Technical Support', 'Delivery Issue', 'Billing Question']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Escalated']
    
    data = []
    for i in range(num_rows):
        created_date = fake.date_between(start_date='-1y', end_date='today')
        
        data.append({
            'ticket_id': f'TKT{str(i+1).zfill(6)}',
            'customer_id': f'CUS{str(random.randint(1, 200)).zfill(5)}',
            'product_id': f'PRD{str(random.randint(1, 120)).zfill(5)}' if random.random() > 0.3 else None,
            'assigned_employee_id': f'EMP{str(random.randint(1, 150)).zfill(5)}',
            'ticket_type': random.choice(ticket_types),
            'priority': random.choice(priorities),
            'status': random.choice(statuses),
            'created_date': created_date,
            'resolved_date': created_date + timedelta(days=random.randint(1, 30)) if random.random() > 0.3 else None,
            'subject': fake.sentence(nb_words=8),
            'description': fake.text(max_nb_chars=200),
            'resolution_notes': fake.text(max_nb_chars=150) if random.random() > 0.4 else None,
            'satisfaction_rating': random.choice([1, 2, 3, 4, 5, None]),
            'channel': random.choice(['Phone', 'Email', 'Chat', 'In-Person'])
        })
    
    return pd.DataFrame(data)


def generate_marketing_campaigns(num_rows=40):
    """Generate marketing campaign data"""
    channels = ['Email', 'Social Media', 'TV', 'Radio', 'Print', 'Online Ads', 'Events']
    
    data = []
    for i in range(num_rows):
        budget = random.randint(5000, 100000)
        revenue = int(budget * random.uniform(0.5, 4.0))
        
        data.append({
            'campaign_id': f'CMP{str(i+1).zfill(5)}',
            'campaign_name': f'{fake.catch_phrase()} {random.choice(["Sale", "Promotion", "Launch", "Event"])}',
            'channel': random.choice(channels),
            'start_date': fake.date_between(start_date='-2y', end_date='today'),
            'end_date': fake.date_between(start_date='today', end_date='+6m'),
            'budget': budget,
            'actual_spend': int(budget * random.uniform(0.8, 1.1)),
            'impressions': random.randint(10000, 1000000),
            'clicks': random.randint(500, 50000),
            'conversions': random.randint(50, 5000),
            'revenue_generated': revenue,
            'roi': round((revenue - budget) / budget * 100, 2),
            'target_audience': random.choice(['All', '18-35', '36-50', '50+', 'Business']),
            'status': random.choice(['Planned', 'Active', 'Completed', 'Paused'])
        })
    
    return pd.DataFrame(data)


def generate_shipments(num_rows=280):
    """Generate shipment tracking data"""
    carriers = ['FedEx', 'UPS', 'DHL', 'USPS', 'Local Courier']
    statuses = ['In Transit', 'Delivered', 'Pending Pickup', 'Out for Delivery', 'Delayed', 'Returned']
    
    data = []
    for i in range(num_rows):
        ship_date = fake.date_between(start_date='-1y', end_date='today')
        
        data.append({
            'shipment_id': f'SHIP{str(i+1).zfill(6)}',
            'order_id': f'ORD{str(random.randint(1, 300)).zfill(6)}',
            'carrier': random.choice(carriers),
            'tracking_number': fake.bothify(text='??#############'),
            'ship_date': ship_date,
            'estimated_delivery': ship_date + timedelta(days=random.randint(2, 10)),
            'actual_delivery': ship_date + timedelta(days=random.randint(2, 12)) if random.random() > 0.2 else None,
            'origin_city': fake.city(),
            'origin_state': fake.state_abbr(),
            'destination_city': fake.city(),
            'destination_state': fake.state_abbr(),
            'weight_kg': round(random.uniform(1, 100), 2),
            'shipping_cost': round(random.uniform(10, 150), 2),
            'status': random.choice(statuses)
        })
    
    return pd.DataFrame(data)


def generate_warranties(num_rows=250):
    """Generate warranty registration data"""
    data = []
    for i in range(num_rows):
        purchase_date = fake.date_between(start_date='-3y', end_date='today')
        warranty_months = random.choice([6, 12, 24, 36, 60])
        
        data.append({
            'warranty_id': f'WAR{str(i+1).zfill(6)}',
            'product_id': f'PRD{str(random.randint(1, 120)).zfill(5)}',
            'customer_id': f'CUS{str(random.randint(1, 200)).zfill(5)}',
            'purchase_date': purchase_date,
            'warranty_start_date': purchase_date,
            'warranty_end_date': purchase_date + timedelta(days=warranty_months*30),
            'warranty_type': random.choice(['Standard', 'Extended', 'Premium']),
            'coverage_amount': random.randint(500, 5000),
            'registration_date': purchase_date + timedelta(days=random.randint(0, 30)),
            'claim_count': random.randint(0, 3),
            'status': random.choice(['Active', 'Active', 'Active', 'Expired', 'Claimed']),
            'serial_number': fake.bothify(text='SN-########'),
            'notes': fake.sentence() if random.random() > 0.7 else None
        })
    
    return pd.DataFrame(data)


def main():
    """Main function to generate all Excel files"""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("🔄 Generating Excel files for Electronics Appliance Company...")
    print("-" * 60)
    
    # Dictionary to store all dataframes
    datasets = {
        'employees': generate_employees(),
        'products': generate_products(),
        'customers': generate_customers(),
        'sales_orders': generate_sales_orders(),
        'inventory': generate_inventory(),
        'suppliers': generate_suppliers(),
        'financial_transactions': generate_financial_transactions(),
        'payroll': generate_payroll(),
        'customer_service_tickets': generate_customer_service(),
        'marketing_campaigns': generate_marketing_campaigns(),
        'shipments': generate_shipments(),
        'warranties': generate_warranties()
    }
    
    # Save each dataset to Excel
    for name, df in datasets.items():
        file_path = os.path.join(OUTPUT_DIR, f'{name}.xlsx')
        df.to_excel(file_path, index=False, sheet_name=name)
        print(f"✅ Generated: {file_path} ({len(df)} rows, {len(df.columns)} columns)")
    
    print("-" * 60)
    print(f"✨ Successfully generated {len(datasets)} Excel files!")
    print(f"📁 Files saved in: {OUTPUT_DIR}/")
    print("\n📊 Summary:")
    for name, df in datasets.items():
        print(f"   - {name}: {len(df)} rows × {len(df.columns)} columns")
    
    return datasets


if __name__ == "__main__":
    datasets = main()

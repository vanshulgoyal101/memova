"""
Excel Data Generator for Airline Company
Generates 15-25 realistic Excel files with 300-400 rows and 15-25 columns each
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

from src.utils.config import Config

# Initialize Faker
fake = Faker()
Faker.seed(100)
random.seed(100)

# Output directory
config = Config()
OUTPUT_DIR = os.path.join(config.EXCEL_OUTPUT_DIR, 'airline_company')


def generate_aircraft(num_rows=350):
    """Generate aircraft fleet data"""
    aircraft_types = ['Boeing 737', 'Boeing 777', 'Boeing 787', 'Airbus A320', 'Airbus A330', 
                      'Airbus A350', 'Boeing 747', 'Airbus A380', 'Embraer E190', 'Bombardier CRJ900']
    statuses = ['Active', 'Maintenance', 'Storage', 'Active', 'Active', 'Active']
    
    data = []
    for i in range(num_rows):
        aircraft_type = random.choice(aircraft_types)
        purchase_date = fake.date_between(start_date='-15y', end_date='-1y')
        
        data.append({
            'aircraft_id': f'AC{str(i+1).zfill(5)}',
            'registration_number': f'N{random.randint(10000, 99999)}',
            'aircraft_type': aircraft_type,
            'manufacturer': aircraft_type.split()[0],
            'model': aircraft_type.split()[1] if len(aircraft_type.split()) > 1 else 'N/A',
            'seat_capacity': random.randint(150, 450),
            'business_class_seats': random.randint(20, 50),
            'economy_class_seats': random.randint(100, 400),
            'manufacturing_year': random.randint(2005, 2024),
            'purchase_date': purchase_date,
            'purchase_price_millions': round(random.uniform(50, 400), 2),
            'current_value_millions': round(random.uniform(30, 350), 2),
            'last_maintenance_date': fake.date_between(start_date='-6m', end_date='today'),
            'next_maintenance_date': fake.date_between(start_date='today', end_date='+6m'),
            'total_flight_hours': random.randint(5000, 80000),
            'status': random.choice(statuses),
            'home_base': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA']),
            'fuel_capacity_gallons': random.randint(20000, 60000),
            'range_miles': random.randint(2000, 9000),
            'cruise_speed_mph': random.randint(450, 600)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'aircraft.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_pilots(num_rows=400):
    """Generate pilot data"""
    ranks = ['Captain', 'First Officer', 'Senior Captain', 'Training Captain']
    certifications = ['ATP', 'Commercial', 'Multi-Engine', 'Instrument']
    statuses = ['Active', 'On Leave', 'Training', 'Active', 'Active']
    
    data = []
    for i in range(num_rows):
        hire_date = fake.date_between(start_date='-20y', end_date='-1y')
        
        data.append({
            'pilot_id': f'PLT{str(i+1).zfill(5)}',
            'employee_id': f'EMP{str(i+5000).zfill(5)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'rank': random.choice(ranks),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'date_of_birth': fake.date_of_birth(minimum_age=28, maximum_age=65),
            'hire_date': hire_date,
            'years_of_service': (datetime.now() - datetime.strptime(str(hire_date), '%Y-%m-%d')).days // 365,
            'total_flight_hours': random.randint(2000, 25000),
            'certifications': ', '.join(random.sample(certifications, random.randint(2, 4))),
            'base_airport': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA', 'SEA']),
            'salary': random.randint(80000, 350000),
            'bonus': random.randint(5000, 50000),
            'status': random.choice(statuses),
            'license_number': f'L{random.randint(100000, 999999)}',
            'license_expiry': fake.date_between(start_date='today', end_date='+2y'),
            'medical_cert_expiry': fake.date_between(start_date='today', end_date='+1y'),
            'type_ratings': random.choice(['B737, B777', 'A320, A330', 'B787, B777', 'A350, A380']),
            'languages_spoken': random.choice(['English', 'English, Spanish', 'English, French', 'English, Mandarin']),
            'emergency_contact': fake.name(),
            'emergency_phone': fake.phone_number()
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'pilots.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_cabin_crew(num_rows=380):
    """Generate cabin crew data"""
    positions = ['Flight Attendant', 'Lead Flight Attendant', 'Purser', 'Junior Flight Attendant']
    statuses = ['Active', 'On Leave', 'Training', 'Active', 'Active']
    
    data = []
    for i in range(num_rows):
        hire_date = fake.date_between(start_date='-15y', end_date='-6m')
        
        data.append({
            'crew_id': f'CRW{str(i+1).zfill(5)}',
            'employee_id': f'EMP{str(i+6000).zfill(5)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'position': random.choice(positions),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'date_of_birth': fake.date_of_birth(minimum_age=21, maximum_age=60),
            'hire_date': hire_date,
            'years_of_service': (datetime.now() - datetime.strptime(str(hire_date), '%Y-%m-%d')).days // 365,
            'base_airport': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA', 'SEA']),
            'salary': random.randint(35000, 95000),
            'bonus': random.randint(1000, 8000),
            'status': random.choice(statuses),
            'languages_spoken': random.choice(['English', 'English, Spanish', 'English, French', 'English, German', 'English, Japanese']),
            'safety_training_date': fake.date_between(start_date='-1y', end_date='today'),
            'safety_cert_expiry': fake.date_between(start_date='today', end_date='+1y'),
            'total_flights': random.randint(500, 8000),
            'hours_flown': random.randint(2000, 20000),
            'emergency_contact': fake.name(),
            'emergency_phone': fake.phone_number(),
            'uniform_size': random.choice(['XS', 'S', 'M', 'L', 'XL'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'cabin_crew.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_flights(num_rows=400):
    """Generate flight schedule data"""
    airports = ['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA', 'SEA', 'BOS', 'DEN', 
                'LHR', 'CDG', 'FRA', 'NRT', 'HND', 'SIN', 'DXB', 'SYD', 'HKG', 'ICN']
    statuses = ['Scheduled', 'Departed', 'Arrived', 'Delayed', 'Cancelled', 'Scheduled', 'Departed', 'Arrived']
    
    data = []
    for i in range(num_rows):
        origin = random.choice(airports)
        destination = random.choice([a for a in airports if a != origin])
        scheduled_departure = fake.date_time_between(start_date='-30d', end_date='+30d')
        duration_hours = random.uniform(1, 16)
        scheduled_arrival = scheduled_departure + timedelta(hours=duration_hours)
        
        data.append({
            'flight_id': f'FL{str(i+1).zfill(6)}',
            'flight_number': f'AA{random.randint(100, 9999)}',
            'aircraft_id': f'AC{str(random.randint(1, 350)).zfill(5)}',
            'origin_airport': origin,
            'destination_airport': destination,
            'scheduled_departure': scheduled_departure,
            'scheduled_arrival': scheduled_arrival,
            'actual_departure': scheduled_departure + timedelta(minutes=random.randint(-30, 120)) if random.random() > 0.3 else None,
            'actual_arrival': scheduled_arrival + timedelta(minutes=random.randint(-20, 90)) if random.random() > 0.3 else None,
            'status': random.choice(statuses),
            'pilot_id': f'PLT{str(random.randint(1, 400)).zfill(5)}',
            'copilot_id': f'PLT{str(random.randint(1, 400)).zfill(5)}',
            'lead_crew_id': f'CRW{str(random.randint(1, 380)).zfill(5)}',
            'distance_miles': random.randint(200, 8000),
            'duration_hours': round(duration_hours, 2),
            'passengers_booked': random.randint(50, 450),
            'passengers_checkedin': random.randint(40, 450),
            'cargo_weight_lbs': random.randint(1000, 50000),
            'fuel_consumed_gallons': random.randint(2000, 40000),
            'gate_departure': f'{random.choice(["A", "B", "C", "D"])}{random.randint(1, 50)}',
            'gate_arrival': f'{random.choice(["A", "B", "C", "D"])}{random.randint(1, 50)}',
            'weather_departure': random.choice(['Clear', 'Cloudy', 'Rainy', 'Stormy', 'Foggy']),
            'weather_arrival': random.choice(['Clear', 'Cloudy', 'Rainy', 'Stormy', 'Foggy'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'flights.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_passengers(num_rows=350):
    """Generate passenger data"""
    ticket_classes = ['Economy', 'Business', 'First Class', 'Economy', 'Economy']
    statuses = ['Confirmed', 'Checked-In', 'Boarded', 'No-Show', 'Cancelled']
    
    data = []
    for i in range(num_rows):
        booking_date = fake.date_between(start_date='-90d', end_date='today')
        
        data.append({
            'passenger_id': f'PAX{str(i+1).zfill(6)}',
            'booking_reference': f'B{fake.bothify(text="??######").upper()}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'date_of_birth': fake.date_of_birth(minimum_age=1, maximum_age=90),
            'passport_number': fake.bothify(text="??#######").upper(),
            'nationality': fake.country(),
            'flight_id': f'FL{str(random.randint(1, 400)).zfill(6)}',
            'ticket_class': random.choice(ticket_classes),
            'seat_number': f'{random.randint(1, 45)}{random.choice(["A", "B", "C", "D", "E", "F"])}',
            'ticket_price': round(random.uniform(150, 5000), 2),
            'baggage_weight_lbs': random.randint(0, 70),
            'special_meals': random.choice(['None', 'Vegetarian', 'Vegan', 'Halal', 'Kosher', 'Gluten-Free']),
            'frequent_flyer_number': f'FF{random.randint(1000000, 9999999)}' if random.random() > 0.5 else None,
            'miles_earned': random.randint(200, 8000),
            'booking_date': booking_date,
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']),
            'booking_status': random.choice(statuses),
            'emergency_contact': fake.name(),
            'emergency_phone': fake.phone_number()
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'passengers.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_maintenance_records(num_rows=320):
    """Generate aircraft maintenance records"""
    maintenance_types = ['Routine', 'Scheduled', 'Emergency', 'Inspection', 'Repair', 'Overhaul']
    statuses = ['Completed', 'In Progress', 'Scheduled', 'Completed', 'Completed']
    
    data = []
    for i in range(num_rows):
        start_date = fake.date_time_between(start_date='-2y', end_date='now')
        
        data.append({
            'maintenance_id': f'MNT{str(i+1).zfill(6)}',
            'aircraft_id': f'AC{str(random.randint(1, 350)).zfill(5)}',
            'maintenance_type': random.choice(maintenance_types),
            'description': fake.sentence(nb_words=10),
            'start_date': start_date,
            'end_date': start_date + timedelta(days=random.randint(1, 30)),
            'mechanic_id': f'MEC{str(random.randint(1, 200)).zfill(5)}',
            'cost': round(random.uniform(5000, 500000), 2),
            'parts_cost': round(random.uniform(1000, 200000), 2),
            'labor_cost': round(random.uniform(2000, 150000), 2),
            'downtime_hours': random.randint(8, 720),
            'status': random.choice(statuses),
            'priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'work_order_number': f'WO{random.randint(100000, 999999)}',
            'approved_by': fake.name(),
            'completed_by': fake.name() if random.random() > 0.3 else None,
            'notes': fake.text(max_nb_chars=200),
            'next_maintenance_due': fake.date_between(start_date='today', end_date='+1y')
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'maintenance_records.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_airports(num_rows=300):
    """Generate airport information"""
    data = []
    for i in range(num_rows):
        data.append({
            'airport_id': f'APT{str(i+1).zfill(5)}',
            'airport_code': fake.bothify(text='???').upper(),
            'airport_name': f'{fake.city()} International Airport',
            'city': fake.city(),
            'state': fake.state() if random.random() > 0.5 else None,
            'country': fake.country(),
            'latitude': round(random.uniform(-90, 90), 6),
            'longitude': round(random.uniform(-180, 180), 6),
            'elevation_feet': random.randint(0, 15000),
            'timezone': random.choice(['EST', 'CST', 'MST', 'PST', 'GMT', 'CET', 'JST', 'AEST']),
            'number_of_runways': random.randint(1, 6),
            'longest_runway_feet': random.randint(5000, 15000),
            'terminal_count': random.randint(1, 8),
            'annual_passengers_millions': round(random.uniform(0.5, 100), 2),
            'cargo_volume_tons': random.randint(10000, 5000000),
            'hub_for_airline': random.choice(['American', 'Delta', 'United', 'Southwest', 'None']),
            'customs_facility': random.choice(['Yes', 'No']),
            'parking_spaces': random.randint(1000, 50000),
            'ground_transportation': 'Taxi, Uber, Bus, Train'
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'airports.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_revenue(num_rows=360):
    """Generate revenue records"""
    revenue_sources = ['Ticket Sales', 'Baggage Fees', 'Seat Selection', 'In-Flight Sales', 
                       'Cargo', 'Lounge Access', 'Change Fees', 'Premium Services']
    
    data = []
    for i in range(num_rows):
        transaction_date = fake.date_between(start_date='-1y', end_date='-1d')
        
        data.append({
            'revenue_id': f'REV{str(i+1).zfill(6)}',
            'transaction_date': transaction_date,
            'flight_id': f'FL{str(random.randint(1, 400)).zfill(6)}',
            'revenue_source': random.choice(revenue_sources),
            'amount': round(random.uniform(50, 150000), 2),
            'currency': random.choice(['USD', 'EUR', 'GBP', 'JPY']),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'Cash', 'PayPal']),
            'passenger_id': f'PAX{str(random.randint(1, 350)).zfill(6)}' if random.random() > 0.3 else None,
            'booking_reference': f'B{fake.bothify(text="??######").upper()}',
            'commission_paid': round(random.uniform(0, 5000), 2),
            'net_revenue': round(random.uniform(40, 145000), 2),
            'tax_amount': round(random.uniform(5, 15000), 2),
            'refund_amount': round(random.uniform(0, 2000), 2) if random.random() > 0.8 else 0,
            'processed_by': fake.name(),
            'region': random.choice(['North America', 'Europe', 'Asia', 'South America', 'Africa']),
            'notes': fake.text(max_nb_chars=100) if random.random() > 0.7 else ''
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'revenue.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_fuel_consumption(num_rows=330):
    """Generate fuel consumption records"""
    data = []
    for i in range(num_rows):
        data.append({
            'fuel_record_id': f'FUEL{str(i+1).zfill(6)}',
            'flight_id': f'FL{str(random.randint(1, 400)).zfill(6)}',
            'aircraft_id': f'AC{str(random.randint(1, 350)).zfill(5)}',
            'refuel_date': fake.date_time_between(start_date='-6m', end_date='now'),
            'airport_code': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA']),
            'fuel_type': random.choice(['Jet A', 'Jet A-1', 'JP-5', 'JP-8']),
            'quantity_gallons': random.randint(5000, 45000),
            'price_per_gallon': round(random.uniform(2.5, 5.5), 2),
            'total_cost': round(random.uniform(15000, 200000), 2),
            'supplier': random.choice(['Shell Aviation', 'BP Aviation', 'ExxonMobil', 'Chevron']),
            'fuel_efficiency_mpg': round(random.uniform(0.1, 0.5), 3),
            'distance_covered_miles': random.randint(500, 8000),
            'fuel_remaining_gallons': random.randint(2000, 15000),
            'temperature_fahrenheit': random.randint(-40, 100),
            'density_lbs_per_gallon': round(random.uniform(6.5, 6.9), 2),
            'invoice_number': f'INV{random.randint(100000, 999999)}',
            'payment_status': random.choice(['Paid', 'Pending', 'Overdue'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'fuel_consumption.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_ground_staff(num_rows=340):
    """Generate ground staff data"""
    positions = ['Baggage Handler', 'Gate Agent', 'Ramp Agent', 'Customer Service', 
                 'Security', 'Maintenance Crew', 'Cleaners', 'Cargo Handler']
    shifts = ['Morning', 'Afternoon', 'Night', 'Rotating']
    
    data = []
    for i in range(num_rows):
        hire_date = fake.date_between(start_date='-10y', end_date='-1m')
        
        data.append({
            'staff_id': f'GND{str(i+1).zfill(5)}',
            'employee_id': f'EMP{str(i+7000).zfill(5)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'position': random.choice(positions),
            'department': random.choice(['Operations', 'Customer Service', 'Maintenance', 'Security']),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=65),
            'hire_date': hire_date,
            'airport_assigned': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA']),
            'shift': random.choice(shifts),
            'hourly_rate': round(random.uniform(15, 45), 2),
            'overtime_hours_month': random.randint(0, 40),
            'status': random.choice(['Active', 'On Leave', 'Active', 'Active']),
            'supervisor': fake.name(),
            'certifications': random.choice(['Safety', 'Forklift', 'Security Clearance', 'None']),
            'performance_rating': round(random.uniform(2.5, 5.0), 1),
            'emergency_contact': fake.name(),
            'emergency_phone': fake.phone_number(),
            'uniform_size': random.choice(['S', 'M', 'L', 'XL', 'XXL'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'ground_staff.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_baggage(num_rows=370):
    """Generate baggage tracking data"""
    statuses = ['Checked-In', 'Loaded', 'In-Transit', 'Arrived', 'Claimed', 'Lost', 'Delayed']
    
    data = []
    for i in range(num_rows):
        data.append({
            'baggage_id': f'BAG{str(i+1).zfill(7)}',
            'tag_number': f'{random.randint(100000, 999999)}',
            'passenger_id': f'PAX{str(random.randint(1, 350)).zfill(6)}',
            'flight_id': f'FL{str(random.randint(1, 400)).zfill(6)}',
            'weight_lbs': round(random.uniform(10, 70), 1),
            'dimensions_inches': f'{random.randint(18, 30)}x{random.randint(12, 24)}x{random.randint(8, 16)}',
            'bag_type': random.choice(['Checked', 'Carry-On', 'Special']),
            'status': random.choice(statuses),
            'check_in_time': fake.date_time_between(start_date='-30d', end_date='now'),
            'loading_time': fake.date_time_between(start_date='-30d', end_date='now'),
            'arrival_time': fake.date_time_between(start_date='-29d', end_date='now'),
            'claim_time': fake.date_time_between(start_date='-29d', end_date='now') if random.random() > 0.3 else None,
            'origin_airport': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL']),
            'destination_airport': random.choice(['SFO', 'MIA', 'SEA', 'BOS', 'DEN']),
            'current_location': random.choice(['Origin', 'In-Transit', 'Destination', 'Claimed']),
            'handling_fee': round(random.uniform(0, 150), 2),
            'insurance_value': round(random.uniform(0, 5000), 2) if random.random() > 0.7 else 0,
            'special_handling': random.choice(['None', 'Fragile', 'Priority', 'Heavy']),
            'barcode': f'{random.randint(1000000000, 9999999999)}',
            'notes': fake.text(max_nb_chars=100) if random.random() > 0.8 else ''
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'baggage.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_incidents(num_rows=300):
    """Generate safety incidents and reports"""
    incident_types = ['Delay', 'Mechanical', 'Weather', 'Bird Strike', 'Medical Emergency', 
                      'Security', 'Baggage Issue', 'Customer Complaint']
    severities = ['Low', 'Medium', 'High', 'Critical']
    
    data = []
    for i in range(num_rows):
        incident_date = fake.date_time_between(start_date='-1y', end_date='now')
        
        data.append({
            'incident_id': f'INC{str(i+1).zfill(6)}',
            'flight_id': f'FL{str(random.randint(1, 400)).zfill(6)}' if random.random() > 0.2 else None,
            'aircraft_id': f'AC{str(random.randint(1, 350)).zfill(5)}' if random.random() > 0.3 else None,
            'incident_type': random.choice(incident_types),
            'severity': random.choice(severities),
            'incident_date': incident_date,
            'reported_by': fake.name(),
            'reported_by_role': random.choice(['Pilot', 'Crew', 'Ground Staff', 'Passenger', 'Manager']),
            'location': random.choice(['In-Flight', 'Gate', 'Runway', 'Terminal', 'Maintenance']),
            'description': fake.text(max_nb_chars=300),
            'injuries': random.randint(0, 5) if random.random() > 0.9 else 0,
            'damages_usd': round(random.uniform(0, 500000), 2) if random.random() > 0.6 else 0,
            'investigation_status': random.choice(['Open', 'Under Review', 'Closed', 'Pending']),
            'investigated_by': fake.name(),
            'resolution': fake.sentence(nb_words=15) if random.random() > 0.4 else '',
            'preventive_action': fake.sentence(nb_words=12) if random.random() > 0.5 else '',
            'faa_notified': random.choice(['Yes', 'No']),
            'insurance_claim': random.choice(['Yes', 'No']),
            'closed_date': incident_date + timedelta(days=random.randint(1, 90)) if random.random() > 0.4 else None
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'incidents.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_loyalty_program(num_rows=310):
    """Generate frequent flyer loyalty program data"""
    tiers = ['Silver', 'Gold', 'Platinum', 'Diamond']
    
    data = []
    for i in range(num_rows):
        join_date = fake.date_between(start_date='-10y', end_date='-1m')
        
        data.append({
            'member_id': f'FF{str(i+1).zfill(7)}',
            'passenger_id': f'PAX{str(random.randint(1, 350)).zfill(6)}',
            'membership_number': f'{random.randint(10000000, 99999999)}',
            'tier': random.choice(tiers),
            'points_balance': random.randint(0, 500000),
            'lifetime_miles': random.randint(10000, 2000000),
            'tier_miles_ytd': random.randint(0, 150000),
            'join_date': join_date,
            'last_activity_date': fake.date_between(start_date='-3m', end_date='-1d'),
            'status': random.choice(['Active', 'Inactive', 'Suspended', 'Active', 'Active']),
            'companion_passes': random.randint(0, 4),
            'lounge_access': random.choice(['Yes', 'No']),
            'priority_boarding': random.choice(['Yes', 'No']),
            'free_baggage_count': random.randint(0, 3),
            'upgrade_certificates': random.randint(0, 8),
            'points_expiry_date': fake.date_between(start_date='today', end_date='+2y'),
            'email_preferences': random.choice(['All', 'Promotions Only', 'Account Only', 'None']),
            'mobile_app_user': random.choice(['Yes', 'No']),
            'credit_card_linked': random.choice(['Yes', 'No']),
            'referral_count': random.randint(0, 20)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'loyalty_program.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_routes(num_rows=320):
    """Generate flight route information"""
    data = []
    airports = ['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA', 'SEA', 'BOS', 'DEN',
                'LHR', 'CDG', 'FRA', 'NRT', 'SIN', 'DXB', 'SYD', 'HKG']
    
    for i in range(num_rows):
        origin = random.choice(airports)
        destination = random.choice([a for a in airports if a != origin])
        
        data.append({
            'route_id': f'RT{str(i+1).zfill(5)}',
            'origin_airport': origin,
            'destination_airport': destination,
            'distance_miles': random.randint(300, 9000),
            'typical_duration_hours': round(random.uniform(1, 18), 1),
            'flights_per_week': random.randint(1, 35),
            'aircraft_type_used': random.choice(['Boeing 737', 'Boeing 777', 'Airbus A320', 'Airbus A350']),
            'average_load_factor': round(random.uniform(0.6, 0.95), 2),
            'average_ticket_price': round(random.uniform(200, 4000), 2),
            'seasonal_route': random.choice(['Yes', 'No']),
            'competition_level': random.choice(['Low', 'Medium', 'High']),
            'profitability_rating': round(random.uniform(1, 5), 1),
            'fuel_cost_per_flight': round(random.uniform(8000, 120000), 2),
            'crew_cost_per_flight': round(random.uniform(3000, 15000), 2),
            'gate_fees_per_flight': round(random.uniform(500, 5000), 2),
            'total_cost_per_flight': round(random.uniform(15000, 180000), 2),
            'revenue_per_flight': round(random.uniform(20000, 250000), 2),
            'profit_margin_percent': round(random.uniform(-5, 40), 1),
            'on_time_performance': round(random.uniform(0.70, 0.98), 2),
            'cancellation_rate': round(random.uniform(0.01, 0.10), 3)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'routes.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_catering(num_rows=315):
    """Generate in-flight catering data"""
    meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
    classes = ['Economy', 'Business', 'First Class']
    
    data = []
    for i in range(num_rows):
        data.append({
            'catering_id': f'CAT{str(i+1).zfill(6)}',
            'flight_id': f'FL{str(random.randint(1, 400)).zfill(6)}',
            'supplier': random.choice(['Sky Gourmet', 'Gate Gourmet', 'LSG Sky Chefs', 'Flying Food']),
            'meal_type': random.choice(meal_types),
            'class': random.choice(classes),
            'quantity_ordered': random.randint(50, 450),
            'quantity_served': random.randint(40, 450),
            'cost_per_meal': round(random.uniform(5, 85), 2),
            'total_cost': round(random.uniform(500, 25000), 2),
            'special_meals_count': random.randint(0, 30),
            'vegetarian_count': random.randint(5, 50),
            'vegan_count': random.randint(0, 20),
            'gluten_free_count': random.randint(0, 15),
            'beverages_cost': round(random.uniform(200, 3000), 2),
            'alcohol_cost': round(random.uniform(0, 2500), 2),
            'loading_time': fake.time(),
            'temperature_fahrenheit': random.randint(35, 45),
            'quality_rating': round(random.uniform(3.0, 5.0), 1),
            'waste_percentage': round(random.uniform(0, 15), 1),
            'invoice_number': f'CAT-INV{random.randint(100000, 999999)}'
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'catering.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_weather_data(num_rows=305):
    """Generate weather impact data"""
    conditions = ['Clear', 'Cloudy', 'Rainy', 'Stormy', 'Snowy', 'Foggy', 'Windy']
    
    data = []
    for i in range(num_rows):
        observation_time = fake.date_time_between(start_date='-6m', end_date='now')
        
        data.append({
            'weather_id': f'WX{str(i+1).zfill(6)}',
            'airport_code': random.choice(['JFK', 'LAX', 'ORD', 'DFW', 'ATL', 'SFO', 'MIA', 'SEA']),
            'observation_time': observation_time,
            'temperature_fahrenheit': random.randint(-20, 110),
            'wind_speed_mph': random.randint(0, 60),
            'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'visibility_miles': round(random.uniform(0.1, 10), 1),
            'precipitation_inches': round(random.uniform(0, 3), 2),
            'condition': random.choice(conditions),
            'pressure_inches_hg': round(random.uniform(28.5, 31.0), 2),
            'humidity_percent': random.randint(20, 100),
            'dew_point_fahrenheit': random.randint(-30, 80),
            'cloud_ceiling_feet': random.randint(0, 25000),
            'flight_delays_caused': random.randint(0, 50),
            'flights_cancelled': random.randint(0, 15),
            'flights_diverted': random.randint(0, 8),
            'alert_level': random.choice(['None', 'Advisory', 'Warning', 'Severe']),
            'forecast_accuracy': round(random.uniform(0.7, 0.99), 2)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'weather_data.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def main():
    """Generate all airline company Excel files"""
    print("\n" + "=" * 70)
    print("  ✈️  AIRLINE COMPANY - DATA GENERATION")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate all datasets
    datasets = [
        generate_aircraft,
        generate_pilots,
        generate_cabin_crew,
        generate_flights,
        generate_passengers,
        generate_maintenance_records,
        generate_airports,
        generate_revenue,
        generate_fuel_consumption,
        generate_ground_staff,
        generate_baggage,
        generate_incidents,
        generate_loyalty_program,
        generate_routes,
        generate_catering,
        generate_weather_data
    ]
    
    total_rows = 0
    for dataset_func in datasets:
        df = dataset_func()
        total_rows += len(df)
    
    print("\n" + "=" * 70)
    print(f"  ✨ Successfully generated {len(datasets)} Excel files!")
    print(f"  📁 Files saved in: {OUTPUT_DIR}/")
    print(f"  📊 Total rows: {total_rows:,}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

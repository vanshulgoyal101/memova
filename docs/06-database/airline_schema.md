# 📊 Electronics Appliance Company - Database Schema

**Generated:** 2025-11-01 12:55:34

**Database:** /Volumes/Extreme SSD/code/sql schema/data/database/airline_company.db

**Total Tables:** 16

---

## 📑 Table of Contents

1. [Aircraft](#aircraft)
2. [Airports](#airports)
3. [Baggage](#baggage)
4. [Cabin Crew](#cabin_crew)
5. [Catering](#catering)
6. [Flights](#flights)
7. [Fuel Consumption](#fuel_consumption)
8. [Ground Staff](#ground_staff)
9. [Incidents](#incidents)
10. [Loyalty Program](#loyalty_program)
11. [Maintenance Records](#maintenance_records)
12. [Passengers](#passengers)
13. [Pilots](#pilots)
14. [Revenue](#revenue)
15. [Routes](#routes)
16. [Weather Data](#weather_data)

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

### <a id='aircraft'></a>Aircraft

**Description:** No description available.

**Row Count:** 350

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `aircraft_id` | TEXT | Yes | NULL |  | Unique identifier |
| `registration_number` | TEXT | Yes | NULL |  | Registration Number |
| `aircraft_type` | TEXT | Yes | NULL |  | Aircraft Type |
| `manufacturer` | TEXT | Yes | NULL |  | Manufacturer |
| `model` | TEXT | Yes | NULL |  | Model |
| `seat_capacity` | BIGINT | Yes | NULL |  | City name |
| `business_class_seats` | BIGINT | Yes | NULL |  | Business Class Seats |
| `economy_class_seats` | BIGINT | Yes | NULL |  | Economy Class Seats |
| `manufacturing_year` | BIGINT | Yes | NULL |  | Manufacturing Year |
| `purchase_date` | DATETIME | Yes | NULL |  | Date |
| `purchase_price_millions` | FLOAT | Yes | NULL |  | Price |
| `current_value_millions` | FLOAT | Yes | NULL |  | Current Value Millions |
| `last_maintenance_date` | DATETIME | Yes | NULL |  | Date |
| `next_maintenance_date` | DATETIME | Yes | NULL |  | Date |
| `total_flight_hours` | BIGINT | Yes | NULL |  | Total Flight Hours |
| `status` | TEXT | Yes | NULL |  | Current status |
| `home_base` | TEXT | Yes | NULL |  | Home Base |
| `fuel_capacity_gallons` | BIGINT | Yes | NULL |  | City name |
| `range_miles` | BIGINT | Yes | NULL |  | Range Miles |
| `cruise_speed_mph` | BIGINT | Yes | NULL |  | Cruise Speed Mph |

**Sample Data:**
```
aircraft_id | registration_number | aircraft_type | manufacturer | model
----------------------------------------------------------------------------------
AC00001 | N64715 | Boeing 737 | Boeing | 737
AC00002 | N29543 | Airbus A380 | Airbus | A380
AC00003 | N96985 | Boeing 737 | Boeing | 737

... and 15 more columns
```

---

### <a id='airports'></a>Airports

**Description:** No description available.

**Row Count:** 300

**Column Count:** 19

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `airport_id` | TEXT | Yes | NULL |  | Unique identifier |
| `airport_code` | TEXT | Yes | NULL |  | Airport Code |
| `airport_name` | TEXT | Yes | NULL |  | Name |
| `city` | TEXT | Yes | NULL |  | City name |
| `state` | TEXT | Yes | NULL |  | State code |
| `country` | TEXT | Yes | NULL |  | Country |
| `latitude` | FLOAT | Yes | NULL |  | Latitude |
| `longitude` | FLOAT | Yes | NULL |  | Longitude |
| `elevation_feet` | BIGINT | Yes | NULL |  | Elevation Feet |
| `timezone` | TEXT | Yes | NULL |  | Timezone |
| `number_of_runways` | BIGINT | Yes | NULL |  | Number Of Runways |
| `longest_runway_feet` | BIGINT | Yes | NULL |  | Longest Runway Feet |
| `terminal_count` | BIGINT | Yes | NULL |  | Terminal Count |
| `annual_passengers_millions` | FLOAT | Yes | NULL |  | Annual Passengers Millions |
| `cargo_volume_tons` | BIGINT | Yes | NULL |  | Cargo Volume Tons |
| `hub_for_airline` | TEXT | Yes | NULL |  | Hub For Airline |
| `customs_facility` | TEXT | Yes | NULL |  | Customs Facility |
| `parking_spaces` | BIGINT | Yes | NULL |  | Parking Spaces |
| `ground_transportation` | TEXT | Yes | NULL |  | Ground Transportation |

**Sample Data:**
```
airport_id | airport_code | airport_name | city | state
-----------------------------------------------------------------
APT00001 | SRC | Christopherfurt Inte | Port Nancy | Colorado
APT00002 | PJT | Taylorshire Internat | Tinaland | Texas
APT00003 | TXU | Theresatown Internat | North Natalie | None

... and 14 more columns
```

---

### <a id='baggage'></a>Baggage

**Description:** No description available.

**Row Count:** 370

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `baggage_id` | TEXT | Yes | NULL |  | Unique identifier |
| `tag_number` | BIGINT | Yes | NULL |  | Tag Number |
| `passenger_id` | TEXT | Yes | NULL |  | Unique identifier |
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `weight_lbs` | FLOAT | Yes | NULL |  | Weight Lbs |
| `dimensions_inches` | TEXT | Yes | NULL |  | Dimensions Inches |
| `bag_type` | TEXT | Yes | NULL |  | Bag Type |
| `status` | TEXT | Yes | NULL |  | Current status |
| `check_in_time` | DATETIME | Yes | NULL |  | Check In Time |
| `loading_time` | DATETIME | Yes | NULL |  | Loading Time |
| `arrival_time` | DATETIME | Yes | NULL |  | Arrival Time |
| `claim_time` | DATETIME | Yes | NULL |  | Claim Time |
| `origin_airport` | TEXT | Yes | NULL |  | Origin Airport |
| `destination_airport` | TEXT | Yes | NULL |  | Destination Airport |
| `current_location` | TEXT | Yes | NULL |  | Current Location |
| `handling_fee` | FLOAT | Yes | NULL |  | Handling Fee |
| `insurance_value` | FLOAT | Yes | NULL |  | Insurance Value |
| `special_handling` | TEXT | Yes | NULL |  | Special Handling |
| `barcode` | BIGINT | Yes | NULL |  | Barcode |
| `notes` | TEXT | Yes | NULL |  | Notes |

**Sample Data:**
```
baggage_id | tag_number | passenger_id | flight_id | weight_lbs
-------------------------------------------------------------------------
BAG0000001 | 168353 | PAX000205 | FL000244 | 16.1
BAG0000002 | 902496 | PAX000145 | FL000252 | 28.1
BAG0000003 | 862175 | PAX000300 | FL000341 | 41.7

... and 15 more columns
```

---

### <a id='cabin_crew'></a>Cabin Crew

**Description:** No description available.

**Row Count:** 380

**Column Count:** 22

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `crew_id` | TEXT | Yes | NULL |  | Unique identifier |
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `position` | TEXT | Yes | NULL |  | Position |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `date_of_birth` | DATETIME | Yes | NULL |  | Date |
| `hire_date` | DATETIME | Yes | NULL |  | Date |
| `years_of_service` | BIGINT | Yes | NULL |  | Years Of Service |
| `base_airport` | TEXT | Yes | NULL |  | Base Airport |
| `salary` | BIGINT | Yes | NULL |  | Salary |
| `bonus` | BIGINT | Yes | NULL |  | Bonus |
| `status` | TEXT | Yes | NULL |  | Current status |
| `languages_spoken` | TEXT | Yes | NULL |  | Languages Spoken |
| `safety_training_date` | DATETIME | Yes | NULL |  | Date |
| `safety_cert_expiry` | DATETIME | Yes | NULL |  | Safety Cert Expiry |
| `total_flights` | BIGINT | Yes | NULL |  | Total Flights |
| `hours_flown` | BIGINT | Yes | NULL |  | Hours Flown |
| `emergency_contact` | TEXT | Yes | NULL |  | Emergency Contact |
| `emergency_phone` | TEXT | Yes | NULL |  | Phone number |
| `uniform_size` | TEXT | Yes | NULL |  | Uniform Size |

**Sample Data:**
```
crew_id | employee_id | first_name | last_name | position
-------------------------------------------------------------------
CRW00001 | EMP06000 | Billy | Davis | Lead Flight Attendan
CRW00002 | EMP06001 | Brenda | Hernandez | Junior Flight Attend
CRW00003 | EMP06002 | Matthew | Pittman | Lead Flight Attendan

... and 17 more columns
```

---

### <a id='catering'></a>Catering

**Description:** No description available.

**Row Count:** 315

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `catering_id` | TEXT | Yes | NULL |  | Unique identifier |
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `supplier` | TEXT | Yes | NULL |  | Supplier |
| `meal_type` | TEXT | Yes | NULL |  | Meal Type |
| `class` | TEXT | Yes | NULL |  | Class |
| `quantity_ordered` | BIGINT | Yes | NULL |  | Quantity |
| `quantity_served` | BIGINT | Yes | NULL |  | Quantity |
| `cost_per_meal` | FLOAT | Yes | NULL |  | Cost Per Meal |
| `total_cost` | FLOAT | Yes | NULL |  | Total Cost |
| `special_meals_count` | BIGINT | Yes | NULL |  | Special Meals Count |
| `vegetarian_count` | BIGINT | Yes | NULL |  | Vegetarian Count |
| `vegan_count` | BIGINT | Yes | NULL |  | Vegan Count |
| `gluten_free_count` | BIGINT | Yes | NULL |  | Gluten Free Count |
| `beverages_cost` | FLOAT | Yes | NULL |  | Beverages Cost |
| `alcohol_cost` | FLOAT | Yes | NULL |  | Alcohol Cost |
| `loading_time` | TEXT | Yes | NULL |  | Loading Time |
| `temperature_fahrenheit` | BIGINT | Yes | NULL |  | Temperature Fahrenheit |
| `quality_rating` | FLOAT | Yes | NULL |  | Quality Rating |
| `waste_percentage` | FLOAT | Yes | NULL |  | Waste Percentage |
| `invoice_number` | TEXT | Yes | NULL |  | Invoice Number |

**Sample Data:**
```
catering_id | flight_id | supplier | meal_type | class
----------------------------------------------------------------
CAT000001 | FL000150 | LSG Sky Chefs | Dinner | First Class
CAT000002 | FL000149 | LSG Sky Chefs | Dinner | First Class
CAT000003 | FL000138 | Flying Food | Breakfast | Business

... and 15 more columns
```

---

### <a id='flights'></a>Flights

**Description:** No description available.

**Row Count:** 400

**Column Count:** 23

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `flight_number` | TEXT | Yes | NULL |  | Flight Number |
| `aircraft_id` | TEXT | Yes | NULL |  | Unique identifier |
| `origin_airport` | TEXT | Yes | NULL |  | Origin Airport |
| `destination_airport` | TEXT | Yes | NULL |  | Destination Airport |
| `scheduled_departure` | DATETIME | Yes | NULL |  | Scheduled Departure |
| `scheduled_arrival` | DATETIME | Yes | NULL |  | Scheduled Arrival |
| `actual_departure` | DATETIME | Yes | NULL |  | Actual Departure |
| `actual_arrival` | DATETIME | Yes | NULL |  | Actual Arrival |
| `status` | TEXT | Yes | NULL |  | Current status |
| `pilot_id` | TEXT | Yes | NULL |  | Unique identifier |
| `copilot_id` | TEXT | Yes | NULL |  | Unique identifier |
| `lead_crew_id` | TEXT | Yes | NULL |  | Unique identifier |
| `distance_miles` | BIGINT | Yes | NULL |  | Distance Miles |
| `duration_hours` | FLOAT | Yes | NULL |  | Duration Hours |
| `passengers_booked` | BIGINT | Yes | NULL |  | Passengers Booked |
| `passengers_checkedin` | BIGINT | Yes | NULL |  | Passengers Checkedin |
| `cargo_weight_lbs` | BIGINT | Yes | NULL |  | Cargo Weight Lbs |
| `fuel_consumed_gallons` | BIGINT | Yes | NULL |  | Fuel Consumed Gallons |
| `gate_departure` | TEXT | Yes | NULL |  | Gate Departure |
| `gate_arrival` | TEXT | Yes | NULL |  | Gate Arrival |
| `weather_departure` | TEXT | Yes | NULL |  | Weather Departure |
| `weather_arrival` | TEXT | Yes | NULL |  | Weather Arrival |

**Sample Data:**
```
flight_id | flight_number | aircraft_id | origin_airport | destination_airport
----------------------------------------------------------------------------------------
FL000001 | AA9267 | AC00152 | SFO | LAX
FL000002 | AA9151 | AC00320 | DXB | MIA
FL000003 | AA244 | AC00267 | BOS | ATL

... and 18 more columns
```

---

### <a id='fuel_consumption'></a>Fuel Consumption

**Description:** No description available.

**Row Count:** 330

**Column Count:** 17

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `fuel_record_id` | TEXT | Yes | NULL |  | Unique identifier |
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `aircraft_id` | TEXT | Yes | NULL |  | Unique identifier |
| `refuel_date` | DATETIME | Yes | NULL |  | Date |
| `airport_code` | TEXT | Yes | NULL |  | Airport Code |
| `fuel_type` | TEXT | Yes | NULL |  | Fuel Type |
| `quantity_gallons` | BIGINT | Yes | NULL |  | Quantity |
| `price_per_gallon` | FLOAT | Yes | NULL |  | Price |
| `total_cost` | FLOAT | Yes | NULL |  | Total Cost |
| `supplier` | TEXT | Yes | NULL |  | Supplier |
| `fuel_efficiency_mpg` | FLOAT | Yes | NULL |  | Fuel Efficiency Mpg |
| `distance_covered_miles` | BIGINT | Yes | NULL |  | Distance Covered Miles |
| `fuel_remaining_gallons` | BIGINT | Yes | NULL |  | Fuel Remaining Gallons |
| `temperature_fahrenheit` | BIGINT | Yes | NULL |  | Temperature Fahrenheit |
| `density_lbs_per_gallon` | FLOAT | Yes | NULL |  | Density Lbs Per Gallon |
| `invoice_number` | TEXT | Yes | NULL |  | Invoice Number |
| `payment_status` | TEXT | Yes | NULL |  | Current status |

**Sample Data:**
```
fuel_record_id | flight_id | aircraft_id | refuel_date | airport_code
-------------------------------------------------------------------------------
FUEL000001 | FL000264 | AC00201 | 2025-11-01 12:54:15. | SFO
FUEL000002 | FL000018 | AC00206 | 2025-11-01 12:50:11. | ORD
FUEL000003 | FL000128 | AC00274 | 2025-11-01 12:55:01. | DFW

... and 12 more columns
```

---

### <a id='ground_staff'></a>Ground Staff

**Description:** No description available.

**Row Count:** 340

**Column Count:** 21

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `staff_id` | TEXT | Yes | NULL |  | Unique identifier |
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `position` | TEXT | Yes | NULL |  | Position |
| `department` | TEXT | Yes | NULL |  | Department |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `date_of_birth` | DATETIME | Yes | NULL |  | Date |
| `hire_date` | DATETIME | Yes | NULL |  | Date |
| `airport_assigned` | TEXT | Yes | NULL |  | Airport Assigned |
| `shift` | TEXT | Yes | NULL |  | Shift |
| `hourly_rate` | FLOAT | Yes | NULL |  | Hourly Rate |
| `overtime_hours_month` | BIGINT | Yes | NULL |  | Overtime Hours Month |
| `status` | TEXT | Yes | NULL |  | Current status |
| `supervisor` | TEXT | Yes | NULL |  | Supervisor |
| `certifications` | TEXT | Yes | NULL |  | Certifications |
| `performance_rating` | FLOAT | Yes | NULL |  | Performance Rating |
| `emergency_contact` | TEXT | Yes | NULL |  | Emergency Contact |
| `emergency_phone` | TEXT | Yes | NULL |  | Phone number |
| `uniform_size` | TEXT | Yes | NULL |  | Uniform Size |

**Sample Data:**
```
staff_id | employee_id | first_name | last_name | position
--------------------------------------------------------------------
GND00001 | EMP07000 | Lance | Coffey | Ramp Agent
GND00002 | EMP07001 | Kristen | Moyer | Ramp Agent
GND00003 | EMP07002 | Misty | Ross | Maintenance Crew

... and 16 more columns
```

---

### <a id='incidents'></a>Incidents

**Description:** No description available.

**Row Count:** 300

**Column Count:** 19

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `incident_id` | TEXT | Yes | NULL |  | Unique identifier |
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `aircraft_id` | TEXT | Yes | NULL |  | Unique identifier |
| `incident_type` | TEXT | Yes | NULL |  | Unique identifier |
| `severity` | TEXT | Yes | NULL |  | Severity |
| `incident_date` | DATETIME | Yes | NULL |  | Unique identifier |
| `reported_by` | TEXT | Yes | NULL |  | Reported By |
| `reported_by_role` | TEXT | Yes | NULL |  | Reported By Role |
| `location` | TEXT | Yes | NULL |  | Location |
| `description` | TEXT | Yes | NULL |  | Description |
| `injuries` | BIGINT | Yes | NULL |  | Injuries |
| `damages_usd` | FLOAT | Yes | NULL |  | Damages Usd |
| `investigation_status` | TEXT | Yes | NULL |  | Current status |
| `investigated_by` | TEXT | Yes | NULL |  | Investigated By |
| `resolution` | TEXT | Yes | NULL |  | Resolution |
| `preventive_action` | TEXT | Yes | NULL |  | Preventive Action |
| `faa_notified` | TEXT | Yes | NULL |  | Faa Notified |
| `insurance_claim` | TEXT | Yes | NULL |  | Insurance Claim |
| `closed_date` | DATETIME | Yes | NULL |  | Date |

**Sample Data:**
```
incident_id | flight_id | aircraft_id | incident_type | severity
--------------------------------------------------------------------------
INC000001 | FL000220 | None | Customer Complaint | Medium
INC000002 | None | AC00110 | Delay | Medium
INC000003 | None | AC00010 | Medical Emergency | Critical

... and 14 more columns
```

---

### <a id='loyalty_program'></a>Loyalty Program

**Description:** No description available.

**Row Count:** 310

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `member_id` | TEXT | Yes | NULL |  | Unique identifier |
| `passenger_id` | TEXT | Yes | NULL |  | Unique identifier |
| `membership_number` | BIGINT | Yes | NULL |  | Membership Number |
| `tier` | TEXT | Yes | NULL |  | Tier |
| `points_balance` | BIGINT | Yes | NULL |  | Points Balance |
| `lifetime_miles` | BIGINT | Yes | NULL |  | Lifetime Miles |
| `tier_miles_ytd` | BIGINT | Yes | NULL |  | Tier Miles Ytd |
| `join_date` | DATETIME | Yes | NULL |  | Date |
| `last_activity_date` | DATETIME | Yes | NULL |  | Date |
| `status` | TEXT | Yes | NULL |  | Current status |
| `companion_passes` | BIGINT | Yes | NULL |  | Companion Passes |
| `lounge_access` | TEXT | Yes | NULL |  | Lounge Access |
| `priority_boarding` | TEXT | Yes | NULL |  | Priority Boarding |
| `free_baggage_count` | BIGINT | Yes | NULL |  | Free Baggage Count |
| `upgrade_certificates` | BIGINT | Yes | NULL |  | Upgrade Certificates |
| `points_expiry_date` | DATETIME | Yes | NULL |  | Date |
| `email_preferences` | TEXT | Yes | NULL |  | Email address |
| `mobile_app_user` | TEXT | Yes | NULL |  | Mobile App User |
| `credit_card_linked` | TEXT | Yes | NULL |  | Credit Card Linked |
| `referral_count` | BIGINT | Yes | NULL |  | Referral Count |

**Sample Data:**
```
member_id | passenger_id | membership_number | tier | points_balance
------------------------------------------------------------------------------
FF0000001 | PAX000288 | 10711613 | Diamond | 195689
FF0000002 | PAX000336 | 10260845 | Platinum | 292100
FF0000003 | PAX000195 | 23850754 | Platinum | 420832

... and 15 more columns
```

---

### <a id='maintenance_records'></a>Maintenance Records

**Description:** No description available.

**Row Count:** 320

**Column Count:** 18

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `maintenance_id` | TEXT | Yes | NULL |  | Unique identifier |
| `aircraft_id` | TEXT | Yes | NULL |  | Unique identifier |
| `maintenance_type` | TEXT | Yes | NULL |  | Maintenance Type |
| `description` | TEXT | Yes | NULL |  | Description |
| `start_date` | DATETIME | Yes | NULL |  | Date |
| `end_date` | DATETIME | Yes | NULL |  | Date |
| `mechanic_id` | TEXT | Yes | NULL |  | Unique identifier |
| `cost` | FLOAT | Yes | NULL |  | Cost |
| `parts_cost` | FLOAT | Yes | NULL |  | Parts Cost |
| `labor_cost` | FLOAT | Yes | NULL |  | Labor Cost |
| `downtime_hours` | BIGINT | Yes | NULL |  | Downtime Hours |
| `status` | TEXT | Yes | NULL |  | Current status |
| `priority` | TEXT | Yes | NULL |  | Priority |
| `work_order_number` | TEXT | Yes | NULL |  | Work Order Number |
| `approved_by` | TEXT | Yes | NULL |  | Approved By |
| `completed_by` | TEXT | Yes | NULL |  | Completed By |
| `notes` | TEXT | Yes | NULL |  | Notes |
| `next_maintenance_due` | DATETIME | Yes | NULL |  | Next Maintenance Due |

**Sample Data:**
```
maintenance_id | aircraft_id | maintenance_type | description | start_date
------------------------------------------------------------------------------------
MNT000001 | AC00056 | Emergency | Last traditional dev | 2024-03-12 04:33:12.
MNT000002 | AC00102 | Scheduled | Scene rather respond | 2025-04-01 10:45:37.
MNT000003 | AC00256 | Overhaul | Exist medical servic | 2025-07-12 05:11:54.

... and 13 more columns
```

---

### <a id='passengers'></a>Passengers

**Description:** No description available.

**Row Count:** 350

**Column Count:** 22

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `passenger_id` | TEXT | Yes | NULL |  | Unique identifier |
| `booking_reference` | TEXT | Yes | NULL |  | Booking Reference |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `date_of_birth` | DATETIME | Yes | NULL |  | Date |
| `passport_number` | TEXT | Yes | NULL |  | Passport Number |
| `nationality` | TEXT | Yes | NULL |  | Nationality |
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `ticket_class` | TEXT | Yes | NULL |  | Ticket Class |
| `seat_number` | TEXT | Yes | NULL |  | Seat Number |
| `ticket_price` | FLOAT | Yes | NULL |  | Price |
| `baggage_weight_lbs` | BIGINT | Yes | NULL |  | Baggage Weight Lbs |
| `special_meals` | TEXT | Yes | NULL |  | Special Meals |
| `frequent_flyer_number` | TEXT | Yes | NULL |  | Frequent Flyer Number |
| `miles_earned` | BIGINT | Yes | NULL |  | Miles Earned |
| `booking_date` | DATETIME | Yes | NULL |  | Date |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |
| `booking_status` | TEXT | Yes | NULL |  | Current status |
| `emergency_contact` | TEXT | Yes | NULL |  | Emergency Contact |
| `emergency_phone` | TEXT | Yes | NULL |  | Phone number |

**Sample Data:**
```
passenger_id | booking_reference | first_name | last_name | email
---------------------------------------------------------------------------
PAX000001 | BUB572463 | Melissa | Alvarez | moorepaul@example.co
PAX000002 | BGK088774 | Bradley | Reid | annareyes@example.or
PAX000003 | BIF666627 | Dillon | Cooper | ryanharper@example.n

... and 17 more columns
```

---

### <a id='pilots'></a>Pilots

**Description:** No description available.

**Row Count:** 400

**Column Count:** 23

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `pilot_id` | TEXT | Yes | NULL |  | Unique identifier |
| `employee_id` | TEXT | Yes | NULL |  | Employee unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `rank` | TEXT | Yes | NULL |  | Rank |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | TEXT | Yes | NULL |  | Phone number |
| `date_of_birth` | DATETIME | Yes | NULL |  | Date |
| `hire_date` | DATETIME | Yes | NULL |  | Date |
| `years_of_service` | BIGINT | Yes | NULL |  | Years Of Service |
| `total_flight_hours` | BIGINT | Yes | NULL |  | Total Flight Hours |
| `certifications` | TEXT | Yes | NULL |  | Certifications |
| `base_airport` | TEXT | Yes | NULL |  | Base Airport |
| `salary` | BIGINT | Yes | NULL |  | Salary |
| `bonus` | BIGINT | Yes | NULL |  | Bonus |
| `status` | TEXT | Yes | NULL |  | Current status |
| `license_number` | TEXT | Yes | NULL |  | License Number |
| `license_expiry` | DATETIME | Yes | NULL |  | License Expiry |
| `medical_cert_expiry` | DATETIME | Yes | NULL |  | Medical Cert Expiry |
| `type_ratings` | TEXT | Yes | NULL |  | Type Ratings |
| `languages_spoken` | TEXT | Yes | NULL |  | Languages Spoken |
| `emergency_contact` | TEXT | Yes | NULL |  | Emergency Contact |
| `emergency_phone` | TEXT | Yes | NULL |  | Phone number |

**Sample Data:**
```
pilot_id | employee_id | first_name | last_name | rank
----------------------------------------------------------------
PLT00001 | EMP05000 | Brian | Gonzalez | First Officer
PLT00002 | EMP05001 | Ashley | Horne | Training Captain
PLT00003 | EMP05002 | Brandon | Owens | Training Captain

... and 18 more columns
```

---

### <a id='revenue'></a>Revenue

**Description:** No description available.

**Row Count:** 360

**Column Count:** 16

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `revenue_id` | TEXT | Yes | NULL |  | Unique identifier |
| `transaction_date` | DATETIME | Yes | NULL |  | Date |
| `flight_id` | TEXT | Yes | NULL |  | Unique identifier |
| `revenue_source` | TEXT | Yes | NULL |  | Revenue Source |
| `amount` | FLOAT | Yes | NULL |  | Amount |
| `currency` | TEXT | Yes | NULL |  | Currency |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |
| `passenger_id` | TEXT | Yes | NULL |  | Unique identifier |
| `booking_reference` | TEXT | Yes | NULL |  | Booking Reference |
| `commission_paid` | FLOAT | Yes | NULL |  | Unique identifier |
| `net_revenue` | FLOAT | Yes | NULL |  | Net Revenue |
| `tax_amount` | FLOAT | Yes | NULL |  | Tax Amount |
| `refund_amount` | FLOAT | Yes | NULL |  | Refund Amount |
| `processed_by` | TEXT | Yes | NULL |  | Processed By |
| `region` | TEXT | Yes | NULL |  | Region |
| `notes` | TEXT | Yes | NULL |  | Notes |

**Sample Data:**
```
revenue_id | transaction_date | flight_id | revenue_source | amount
-----------------------------------------------------------------------------
REV000001 | 2025-05-12 00:00:00. | FL000313 | Cargo | 118268.06
REV000002 | 2024-12-19 00:00:00. | FL000242 | Seat Selection | 93996.0
REV000003 | 2025-02-08 00:00:00. | FL000208 | Seat Selection | 109560.68

... and 11 more columns
```

---

### <a id='routes'></a>Routes

**Description:** No description available.

**Row Count:** 320

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `route_id` | TEXT | Yes | NULL |  | Unique identifier |
| `origin_airport` | TEXT | Yes | NULL |  | Origin Airport |
| `destination_airport` | TEXT | Yes | NULL |  | Destination Airport |
| `distance_miles` | BIGINT | Yes | NULL |  | Distance Miles |
| `typical_duration_hours` | FLOAT | Yes | NULL |  | Typical Duration Hours |
| `flights_per_week` | BIGINT | Yes | NULL |  | Flights Per Week |
| `aircraft_type_used` | TEXT | Yes | NULL |  | Aircraft Type Used |
| `average_load_factor` | FLOAT | Yes | NULL |  | Average Load Factor |
| `average_ticket_price` | FLOAT | Yes | NULL |  | Price |
| `seasonal_route` | TEXT | Yes | NULL |  | Seasonal Route |
| `competition_level` | TEXT | Yes | NULL |  | Competition Level |
| `profitability_rating` | FLOAT | Yes | NULL |  | Profitability Rating |
| `fuel_cost_per_flight` | FLOAT | Yes | NULL |  | Fuel Cost Per Flight |
| `crew_cost_per_flight` | FLOAT | Yes | NULL |  | Crew Cost Per Flight |
| `gate_fees_per_flight` | FLOAT | Yes | NULL |  | Gate Fees Per Flight |
| `total_cost_per_flight` | FLOAT | Yes | NULL |  | Total Cost Per Flight |
| `revenue_per_flight` | FLOAT | Yes | NULL |  | Revenue Per Flight |
| `profit_margin_percent` | FLOAT | Yes | NULL |  | Profit Margin Percent |
| `on_time_performance` | FLOAT | Yes | NULL |  | On Time Performance |
| `cancellation_rate` | FLOAT | Yes | NULL |  | Cancellation Rate |

**Sample Data:**
```
route_id | origin_airport | destination_airport | distance_miles | typical_duration_hours
---------------------------------------------------------------------------------------------------
RT00001 | SFO | LHR | 4579 | 10.6
RT00002 | CDG | LHR | 5980 | 10.6
RT00003 | CDG | HKG | 8689 | 11.4

... and 15 more columns
```

---

### <a id='weather_data'></a>Weather Data

**Description:** No description available.

**Row Count:** 305

**Column Count:** 18

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `weather_id` | TEXT | Yes | NULL |  | Unique identifier |
| `airport_code` | TEXT | Yes | NULL |  | Airport Code |
| `observation_time` | DATETIME | Yes | NULL |  | Observation Time |
| `temperature_fahrenheit` | BIGINT | Yes | NULL |  | Temperature Fahrenheit |
| `wind_speed_mph` | BIGINT | Yes | NULL |  | Wind Speed Mph |
| `wind_direction` | TEXT | Yes | NULL |  | Wind Direction |
| `visibility_miles` | FLOAT | Yes | NULL |  | Visibility Miles |
| `precipitation_inches` | FLOAT | Yes | NULL |  | Precipitation Inches |
| `condition` | TEXT | Yes | NULL |  | Condition |
| `pressure_inches_hg` | FLOAT | Yes | NULL |  | Pressure Inches Hg |
| `humidity_percent` | BIGINT | Yes | NULL |  | Unique identifier |
| `dew_point_fahrenheit` | BIGINT | Yes | NULL |  | Dew Point Fahrenheit |
| `cloud_ceiling_feet` | BIGINT | Yes | NULL |  | Cloud Ceiling Feet |
| `flight_delays_caused` | BIGINT | Yes | NULL |  | Flight Delays Caused |
| `flights_cancelled` | BIGINT | Yes | NULL |  | Flights Cancelled |
| `flights_diverted` | BIGINT | Yes | NULL |  | Flights Diverted |
| `alert_level` | TEXT | Yes | NULL |  | Alert Level |
| `forecast_accuracy` | FLOAT | Yes | NULL |  | Forecast Accuracy |

**Sample Data:**
```
weather_id | airport_code | observation_time | temperature_fahrenheit | wind_speed_mph
------------------------------------------------------------------------------------------------
WX000001 | LAX | 2025-11-01 12:53:53. | 28 | 10
WX000002 | SFO | 2025-11-01 12:53:49. | 25 | 38
WX000003 | SEA | 2025-11-01 12:51:53. | 72 | 43

... and 13 more columns
```

---

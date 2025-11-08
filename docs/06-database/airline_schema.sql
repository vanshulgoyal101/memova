-- Electronics Appliance Company Database Schema
-- Generated: 2025-11-01 12:55:34
-- Total Tables: 16


-- Table: aircraft
CREATE TABLE aircraft (
	aircraft_id TEXT, 
	registration_number TEXT, 
	aircraft_type TEXT, 
	manufacturer TEXT, 
	model TEXT, 
	seat_capacity BIGINT, 
	business_class_seats BIGINT, 
	economy_class_seats BIGINT, 
	manufacturing_year BIGINT, 
	purchase_date DATETIME, 
	purchase_price_millions FLOAT, 
	current_value_millions FLOAT, 
	last_maintenance_date DATETIME, 
	next_maintenance_date DATETIME, 
	total_flight_hours BIGINT, 
	status TEXT, 
	home_base TEXT, 
	fuel_capacity_gallons BIGINT, 
	range_miles BIGINT, 
	cruise_speed_mph BIGINT
);


-- Table: airports
CREATE TABLE airports (
	airport_id TEXT, 
	airport_code TEXT, 
	airport_name TEXT, 
	city TEXT, 
	state TEXT, 
	country TEXT, 
	latitude FLOAT, 
	longitude FLOAT, 
	elevation_feet BIGINT, 
	timezone TEXT, 
	number_of_runways BIGINT, 
	longest_runway_feet BIGINT, 
	terminal_count BIGINT, 
	annual_passengers_millions FLOAT, 
	cargo_volume_tons BIGINT, 
	hub_for_airline TEXT, 
	customs_facility TEXT, 
	parking_spaces BIGINT, 
	ground_transportation TEXT
);


-- Table: baggage
CREATE TABLE baggage (
	baggage_id TEXT, 
	tag_number BIGINT, 
	passenger_id TEXT, 
	flight_id TEXT, 
	weight_lbs FLOAT, 
	dimensions_inches TEXT, 
	bag_type TEXT, 
	status TEXT, 
	check_in_time DATETIME, 
	loading_time DATETIME, 
	arrival_time DATETIME, 
	claim_time DATETIME, 
	origin_airport TEXT, 
	destination_airport TEXT, 
	current_location TEXT, 
	handling_fee FLOAT, 
	insurance_value FLOAT, 
	special_handling TEXT, 
	barcode BIGINT, 
	notes TEXT
);


-- Table: cabin_crew
CREATE TABLE cabin_crew (
	crew_id TEXT, 
	employee_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	position TEXT, 
	email TEXT, 
	phone TEXT, 
	date_of_birth DATETIME, 
	hire_date DATETIME, 
	years_of_service BIGINT, 
	base_airport TEXT, 
	salary BIGINT, 
	bonus BIGINT, 
	status TEXT, 
	languages_spoken TEXT, 
	safety_training_date DATETIME, 
	safety_cert_expiry DATETIME, 
	total_flights BIGINT, 
	hours_flown BIGINT, 
	emergency_contact TEXT, 
	emergency_phone TEXT, 
	uniform_size TEXT
);


-- Table: catering
CREATE TABLE catering (
	catering_id TEXT, 
	flight_id TEXT, 
	supplier TEXT, 
	meal_type TEXT, 
	class TEXT, 
	quantity_ordered BIGINT, 
	quantity_served BIGINT, 
	cost_per_meal FLOAT, 
	total_cost FLOAT, 
	special_meals_count BIGINT, 
	vegetarian_count BIGINT, 
	vegan_count BIGINT, 
	gluten_free_count BIGINT, 
	beverages_cost FLOAT, 
	alcohol_cost FLOAT, 
	loading_time TEXT, 
	temperature_fahrenheit BIGINT, 
	quality_rating FLOAT, 
	waste_percentage FLOAT, 
	invoice_number TEXT
);


-- Table: flights
CREATE TABLE flights (
	flight_id TEXT, 
	flight_number TEXT, 
	aircraft_id TEXT, 
	origin_airport TEXT, 
	destination_airport TEXT, 
	scheduled_departure DATETIME, 
	scheduled_arrival DATETIME, 
	actual_departure DATETIME, 
	actual_arrival DATETIME, 
	status TEXT, 
	pilot_id TEXT, 
	copilot_id TEXT, 
	lead_crew_id TEXT, 
	distance_miles BIGINT, 
	duration_hours FLOAT, 
	passengers_booked BIGINT, 
	passengers_checkedin BIGINT, 
	cargo_weight_lbs BIGINT, 
	fuel_consumed_gallons BIGINT, 
	gate_departure TEXT, 
	gate_arrival TEXT, 
	weather_departure TEXT, 
	weather_arrival TEXT
);


-- Table: fuel_consumption
CREATE TABLE fuel_consumption (
	fuel_record_id TEXT, 
	flight_id TEXT, 
	aircraft_id TEXT, 
	refuel_date DATETIME, 
	airport_code TEXT, 
	fuel_type TEXT, 
	quantity_gallons BIGINT, 
	price_per_gallon FLOAT, 
	total_cost FLOAT, 
	supplier TEXT, 
	fuel_efficiency_mpg FLOAT, 
	distance_covered_miles BIGINT, 
	fuel_remaining_gallons BIGINT, 
	temperature_fahrenheit BIGINT, 
	density_lbs_per_gallon FLOAT, 
	invoice_number TEXT, 
	payment_status TEXT
);


-- Table: ground_staff
CREATE TABLE ground_staff (
	staff_id TEXT, 
	employee_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	position TEXT, 
	department TEXT, 
	email TEXT, 
	phone TEXT, 
	date_of_birth DATETIME, 
	hire_date DATETIME, 
	airport_assigned TEXT, 
	shift TEXT, 
	hourly_rate FLOAT, 
	overtime_hours_month BIGINT, 
	status TEXT, 
	supervisor TEXT, 
	certifications TEXT, 
	performance_rating FLOAT, 
	emergency_contact TEXT, 
	emergency_phone TEXT, 
	uniform_size TEXT
);


-- Table: incidents
CREATE TABLE incidents (
	incident_id TEXT, 
	flight_id TEXT, 
	aircraft_id TEXT, 
	incident_type TEXT, 
	severity TEXT, 
	incident_date DATETIME, 
	reported_by TEXT, 
	reported_by_role TEXT, 
	location TEXT, 
	description TEXT, 
	injuries BIGINT, 
	damages_usd FLOAT, 
	investigation_status TEXT, 
	investigated_by TEXT, 
	resolution TEXT, 
	preventive_action TEXT, 
	faa_notified TEXT, 
	insurance_claim TEXT, 
	closed_date DATETIME
);


-- Table: loyalty_program
CREATE TABLE loyalty_program (
	member_id TEXT, 
	passenger_id TEXT, 
	membership_number BIGINT, 
	tier TEXT, 
	points_balance BIGINT, 
	lifetime_miles BIGINT, 
	tier_miles_ytd BIGINT, 
	join_date DATETIME, 
	last_activity_date DATETIME, 
	status TEXT, 
	companion_passes BIGINT, 
	lounge_access TEXT, 
	priority_boarding TEXT, 
	free_baggage_count BIGINT, 
	upgrade_certificates BIGINT, 
	points_expiry_date DATETIME, 
	email_preferences TEXT, 
	mobile_app_user TEXT, 
	credit_card_linked TEXT, 
	referral_count BIGINT
);


-- Table: maintenance_records
CREATE TABLE maintenance_records (
	maintenance_id TEXT, 
	aircraft_id TEXT, 
	maintenance_type TEXT, 
	description TEXT, 
	start_date DATETIME, 
	end_date DATETIME, 
	mechanic_id TEXT, 
	cost FLOAT, 
	parts_cost FLOAT, 
	labor_cost FLOAT, 
	downtime_hours BIGINT, 
	status TEXT, 
	priority TEXT, 
	work_order_number TEXT, 
	approved_by TEXT, 
	completed_by TEXT, 
	notes TEXT, 
	next_maintenance_due DATETIME
);


-- Table: passengers
CREATE TABLE passengers (
	passenger_id TEXT, 
	booking_reference TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	email TEXT, 
	phone TEXT, 
	date_of_birth DATETIME, 
	passport_number TEXT, 
	nationality TEXT, 
	flight_id TEXT, 
	ticket_class TEXT, 
	seat_number TEXT, 
	ticket_price FLOAT, 
	baggage_weight_lbs BIGINT, 
	special_meals TEXT, 
	frequent_flyer_number TEXT, 
	miles_earned BIGINT, 
	booking_date DATETIME, 
	payment_method TEXT, 
	booking_status TEXT, 
	emergency_contact TEXT, 
	emergency_phone TEXT
);


-- Table: pilots
CREATE TABLE pilots (
	pilot_id TEXT, 
	employee_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	rank TEXT, 
	email TEXT, 
	phone TEXT, 
	date_of_birth DATETIME, 
	hire_date DATETIME, 
	years_of_service BIGINT, 
	total_flight_hours BIGINT, 
	certifications TEXT, 
	base_airport TEXT, 
	salary BIGINT, 
	bonus BIGINT, 
	status TEXT, 
	license_number TEXT, 
	license_expiry DATETIME, 
	medical_cert_expiry DATETIME, 
	type_ratings TEXT, 
	languages_spoken TEXT, 
	emergency_contact TEXT, 
	emergency_phone TEXT
);


-- Table: revenue
CREATE TABLE revenue (
	revenue_id TEXT, 
	transaction_date DATETIME, 
	flight_id TEXT, 
	revenue_source TEXT, 
	amount FLOAT, 
	currency TEXT, 
	payment_method TEXT, 
	passenger_id TEXT, 
	booking_reference TEXT, 
	commission_paid FLOAT, 
	net_revenue FLOAT, 
	tax_amount FLOAT, 
	refund_amount FLOAT, 
	processed_by TEXT, 
	region TEXT, 
	notes TEXT
);


-- Table: routes
CREATE TABLE routes (
	route_id TEXT, 
	origin_airport TEXT, 
	destination_airport TEXT, 
	distance_miles BIGINT, 
	typical_duration_hours FLOAT, 
	flights_per_week BIGINT, 
	aircraft_type_used TEXT, 
	average_load_factor FLOAT, 
	average_ticket_price FLOAT, 
	seasonal_route TEXT, 
	competition_level TEXT, 
	profitability_rating FLOAT, 
	fuel_cost_per_flight FLOAT, 
	crew_cost_per_flight FLOAT, 
	gate_fees_per_flight FLOAT, 
	total_cost_per_flight FLOAT, 
	revenue_per_flight FLOAT, 
	profit_margin_percent FLOAT, 
	on_time_performance FLOAT, 
	cancellation_rate FLOAT
);


-- Table: weather_data
CREATE TABLE weather_data (
	weather_id TEXT, 
	airport_code TEXT, 
	observation_time DATETIME, 
	temperature_fahrenheit BIGINT, 
	wind_speed_mph BIGINT, 
	wind_direction TEXT, 
	visibility_miles FLOAT, 
	precipitation_inches FLOAT, 
	condition TEXT, 
	pressure_inches_hg FLOAT, 
	humidity_percent BIGINT, 
	dew_point_fahrenheit BIGINT, 
	cloud_ceiling_feet BIGINT, 
	flight_delays_caused BIGINT, 
	flights_cancelled BIGINT, 
	flights_diverted BIGINT, 
	alert_level TEXT, 
	forecast_accuracy FLOAT
);


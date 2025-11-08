-- Electronics Appliance Company Database Schema
-- Generated: 2025-11-01 12:55:36
-- Total Tables: 15


-- Table: assessments
CREATE TABLE assessments (
	assessment_id TEXT, 
	course_id TEXT, 
	assessment_type TEXT, 
	title TEXT, 
	max_score BIGINT, 
	passing_score BIGINT, 
	duration_minutes BIGINT, 
	total_questions BIGINT, 
	difficulty TEXT, 
	is_proctored TEXT, 
	attempts_allowed BIGINT, 
	created_date DATETIME, 
	status TEXT, 
	weightage_percentage BIGINT
);


-- Table: certificates
CREATE TABLE certificates (
	certificate_id TEXT, 
	student_id TEXT, 
	course_id TEXT, 
	enrollment_id TEXT, 
	issue_date DATETIME, 
	certificate_url TEXT, 
	verification_code TEXT, 
	final_grade FLOAT, 
	rank_in_batch BIGINT, 
	total_batch_size BIGINT, 
	skills_earned TEXT, 
	credential_id TEXT, 
	blockchain_verified TEXT
);


-- Table: course_content
CREATE TABLE course_content (
	content_id TEXT, 
	course_id TEXT, 
	module_number BIGINT, 
	lecture_number BIGINT, 
	title TEXT, 
	content_type TEXT, 
	duration_minutes BIGINT, 
	is_free_preview TEXT, 
	order_index BIGINT, 
	upload_date DATETIME, 
	views_count BIGINT, 
	avg_completion_time_minutes BIGINT, 
	difficulty TEXT, 
	resources_url TEXT, 
	transcript_available TEXT
);


-- Table: courses
CREATE TABLE courses (
	course_id TEXT, 
	course_name TEXT, 
	category TEXT, 
	instructor_id TEXT, 
	difficulty_level TEXT, 
	duration_weeks BIGINT, 
	price_inr BIGINT, 
	discount_price_inr BIGINT, 
	language TEXT, 
	rating FLOAT, 
	total_enrollments BIGINT, 
	course_format TEXT, 
	certification TEXT, 
	placement_assistance TEXT, 
	launch_date DATETIME, 
	status TEXT, 
	prerequisites TEXT, 
	total_videos BIGINT, 
	total_hours BIGINT, 
	includes_projects TEXT
);


-- Table: discussion_forums
CREATE TABLE discussion_forums (
	post_id TEXT, 
	course_id TEXT, 
	student_id TEXT, 
	title TEXT, 
	content TEXT, 
	post_date DATETIME, 
	category TEXT, 
	upvotes BIGINT, 
	reply_count BIGINT, 
	views_count BIGINT, 
	is_resolved TEXT, 
	instructor_replied TEXT, 
	tags TEXT, 
	pinned TEXT, 
	last_activity_date DATETIME
);


-- Table: enrollments
CREATE TABLE enrollments (
	enrollment_id TEXT, 
	student_id TEXT, 
	course_id TEXT, 
	enrollment_date DATETIME, 
	completion_date DATETIME, 
	progress_percentage BIGINT, 
	status TEXT, 
	payment_status TEXT, 
	amount_paid_inr BIGINT, 
	discount_applied BIGINT, 
	payment_method TEXT, 
	certificate_issued TEXT, 
	final_grade FLOAT, 
	attendance_percentage FLOAT, 
	feedback_rating FLOAT
);


-- Table: instructors
CREATE TABLE instructors (
	instructor_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	email TEXT, 
	phone BIGINT, 
	specialization TEXT, 
	years_of_experience BIGINT, 
	education_level TEXT, 
	rating FLOAT, 
	total_students_taught BIGINT, 
	total_courses BIGINT, 
	join_date DATETIME, 
	city TEXT, 
	linkedin_profile TEXT, 
	hourly_rate_inr BIGINT, 
	employment_type TEXT, 
	status TEXT, 
	bio TEXT, 
	languages_spoken TEXT
);


-- Table: live_classes
CREATE TABLE live_classes (
	class_id TEXT, 
	course_id TEXT, 
	instructor_id TEXT, 
	title TEXT, 
	scheduled_date DATETIME, 
	duration_minutes BIGINT, 
	meeting_link TEXT, 
	recording_url TEXT, 
	attendees_count BIGINT, 
	max_capacity BIGINT, 
	status TEXT, 
	platform TEXT, 
	chat_transcript_url TEXT, 
	poll_conducted TEXT, 
	avg_rating FLOAT
);


-- Table: mentorship
CREATE TABLE mentorship (
	session_id TEXT, 
	student_id TEXT, 
	mentor_id TEXT, 
	session_date DATETIME, 
	duration_minutes BIGINT, 
	session_type TEXT, 
	meeting_platform TEXT, 
	status TEXT, 
	student_rating FLOAT, 
	feedback TEXT, 
	topics_discussed TEXT, 
	action_items TEXT, 
	follow_up_required TEXT, 
	recording_url TEXT
);


-- Table: partnerships
CREATE TABLE partnerships (
	partnership_id TEXT, 
	company_name TEXT, 
	company_type TEXT, 
	partnership_type TEXT, 
	start_date DATETIME, 
	contract_value_lakhs FLOAT, 
	employees_trained BIGINT, 
	courses_subscribed BIGINT, 
	status TEXT, 
	point_of_contact TEXT, 
	contact_email TEXT, 
	contact_phone BIGINT, 
	city TEXT, 
	renewal_date DATETIME, 
	placements_provided BIGINT, 
	discount_percentage BIGINT
);


-- Table: payments
CREATE TABLE payments (
	payment_id TEXT, 
	student_id TEXT, 
	enrollment_id TEXT, 
	amount_inr BIGINT, 
	payment_method TEXT, 
	payment_status TEXT, 
	transaction_id TEXT, 
	payment_date DATETIME, 
	payment_gateway TEXT, 
	discount_code TEXT, 
	discount_amount_inr FLOAT, 
	gst_amount_inr FLOAT, 
	net_amount_inr FLOAT, 
	refund_status TEXT, 
	invoice_number TEXT, 
	emi_opted TEXT
);


-- Table: placements
CREATE TABLE placements (
	placement_id TEXT, 
	student_id TEXT, 
	company_name TEXT, 
	job_title TEXT, 
	ctc_lakhs FLOAT, 
	placement_date DATETIME, 
	job_location TEXT, 
	job_type TEXT, 
	course_completed TEXT, 
	company_tier TEXT, 
	referral_bonus_given TEXT, 
	employment_status TEXT, 
	interview_rounds BIGINT, 
	offer_letter_date DATETIME, 
	stipend_inr FLOAT
);


-- Table: student_progress
CREATE TABLE student_progress (
	progress_id TEXT, 
	student_id TEXT, 
	course_id TEXT, 
	videos_completed BIGINT, 
	total_videos BIGINT, 
	quizzes_completed BIGINT, 
	total_quizzes BIGINT, 
	assignments_submitted BIGINT, 
	total_assignments BIGINT, 
	progress_percentage FLOAT, 
	time_spent_hours FLOAT, 
	last_accessed_date DATETIME, 
	streak_days BIGINT, 
	certificates_earned BIGINT, 
	skill_badges_earned BIGINT, 
	current_module BIGINT, 
	estimated_completion_date DATETIME, 
	daily_avg_time_minutes BIGINT
);


-- Table: students
CREATE TABLE students (
	student_id TEXT, 
	first_name TEXT, 
	last_name TEXT, 
	email TEXT, 
	phone BIGINT, 
	date_of_birth DATETIME, 
	gender TEXT, 
	city TEXT, 
	state TEXT, 
	current_education TEXT, 
	college_name TEXT, 
	enrollment_date DATETIME, 
	account_status TEXT, 
	referral_code TEXT, 
	linkedin_profile TEXT, 
	github_profile TEXT, 
	career_goal TEXT, 
	previous_experience_years BIGINT, 
	preferred_language TEXT, 
	subscription_tier TEXT
);


-- Table: submissions
CREATE TABLE submissions (
	submission_id TEXT, 
	assessment_id TEXT, 
	student_id TEXT, 
	submitted_date DATETIME, 
	graded_date DATETIME, 
	score_obtained FLOAT, 
	max_score BIGINT, 
	grade TEXT, 
	attempt_number BIGINT, 
	time_taken_minutes BIGINT, 
	status TEXT, 
	feedback TEXT, 
	plagiarism_score FLOAT, 
	submission_url TEXT, 
	late_submission TEXT
);


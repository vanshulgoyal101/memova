# 📊 Electronics Appliance Company - Database Schema

**Generated:** 2025-11-01 12:55:36

**Database:** /Volumes/Extreme SSD/code/sql schema/data/database/edtech_company.db

**Total Tables:** 15

---

## 📑 Table of Contents

1. [Assessments](#assessments)
2. [Certificates](#certificates)
3. [Course Content](#course_content)
4. [Courses](#courses)
5. [Discussion Forums](#discussion_forums)
6. [Enrollments](#enrollments)
7. [Instructors](#instructors)
8. [Live Classes](#live_classes)
9. [Mentorship](#mentorship)
10. [Partnerships](#partnerships)
11. [Payments](#payments)
12. [Placements](#placements)
13. [Student Progress](#student_progress)
14. [Students](#students)
15. [Submissions](#submissions)

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

### <a id='assessments'></a>Assessments

**Description:** No description available.

**Row Count:** 220

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `assessment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `assessment_type` | TEXT | Yes | NULL |  | Assessment Type |
| `title` | TEXT | Yes | NULL |  | Title |
| `max_score` | BIGINT | Yes | NULL |  | Max Score |
| `passing_score` | BIGINT | Yes | NULL |  | Passing Score |
| `duration_minutes` | BIGINT | Yes | NULL |  | Duration Minutes |
| `total_questions` | BIGINT | Yes | NULL |  | Total Questions |
| `difficulty` | TEXT | Yes | NULL |  | Difficulty |
| `is_proctored` | TEXT | Yes | NULL |  | Is Proctored |
| `attempts_allowed` | BIGINT | Yes | NULL |  | Attempts Allowed |
| `created_date` | DATETIME | Yes | NULL |  | Record creation date |
| `status` | TEXT | Yes | NULL |  | Current status |
| `weightage_percentage` | BIGINT | Yes | NULL |  | Weightage Percentage |

**Sample Data:**
```
assessment_id | course_id | assessment_type | title | max_score
-------------------------------------------------------------------------
ASM000001 | CRS00168 | MCQ Test | Cloned interactive c | 20
ASM000002 | CRS00057 | MCQ Test | Re-contextualized mo | 10
ASM000003 | CRS00015 | Assignment | Re-contextualized ec | 50

... and 9 more columns
```

---

### <a id='certificates'></a>Certificates

**Description:** No description available.

**Row Count:** 230

**Column Count:** 13

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `certificate_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `enrollment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `issue_date` | DATETIME | Yes | NULL |  | Date |
| `certificate_url` | TEXT | Yes | NULL |  | Certificate Url |
| `verification_code` | TEXT | Yes | NULL |  | Verification Code |
| `final_grade` | FLOAT | Yes | NULL |  | Final Grade |
| `rank_in_batch` | BIGINT | Yes | NULL |  | Rank In Batch |
| `total_batch_size` | BIGINT | Yes | NULL |  | Total Batch Size |
| `skills_earned` | TEXT | Yes | NULL |  | Skills Earned |
| `credential_id` | TEXT | Yes | NULL |  | Unique identifier |
| `blockchain_verified` | TEXT | Yes | NULL |  | Blockchain Verified |

**Sample Data:**
```
certificate_id | student_id | course_id | enrollment_id | issue_date
------------------------------------------------------------------------------
CERT000001 | STU000160 | CRS00046 | ENR000216 | 2024-11-14 00:00:00.
CERT000002 | STU000279 | CRS00016 | ENR000125 | 2024-10-04 00:00:00.
CERT000003 | STU000226 | CRS00192 | ENR000218 | 2025-01-16 00:00:00.

... and 8 more columns
```

---

### <a id='course_content'></a>Course Content

**Description:** No description available.

**Row Count:** 250

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `content_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `module_number` | BIGINT | Yes | NULL |  | Module Number |
| `lecture_number` | BIGINT | Yes | NULL |  | Lecture Number |
| `title` | TEXT | Yes | NULL |  | Title |
| `content_type` | TEXT | Yes | NULL |  | Content Type |
| `duration_minutes` | BIGINT | Yes | NULL |  | Duration Minutes |
| `is_free_preview` | TEXT | Yes | NULL |  | Is Free Preview |
| `order_index` | BIGINT | Yes | NULL |  | Order Index |
| `upload_date` | DATETIME | Yes | NULL |  | Date |
| `views_count` | BIGINT | Yes | NULL |  | Views Count |
| `avg_completion_time_minutes` | BIGINT | Yes | NULL |  | Avg Completion Time Minutes |
| `difficulty` | TEXT | Yes | NULL |  | Difficulty |
| `resources_url` | TEXT | Yes | NULL |  | Resources Url |
| `transcript_available` | TEXT | Yes | NULL |  | Transcript Available |

**Sample Data:**
```
content_id | course_id | module_number | lecture_number | title
-------------------------------------------------------------------------
CNT000001 | CRS00020 | 6 | 3 | Hands-on empower glo
CNT000002 | CRS00032 | 3 | 3 | Practical brand seam
CNT000003 | CRS00040 | 1 | 8 | Deep Dive into trans

... and 10 more columns
```

---

### <a id='courses'></a>Courses

**Description:** No description available.

**Row Count:** 200

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_name` | TEXT | Yes | NULL |  | Name |
| `category` | TEXT | Yes | NULL |  | Category |
| `instructor_id` | TEXT | Yes | NULL |  | Unique identifier |
| `difficulty_level` | TEXT | Yes | NULL |  | Difficulty Level |
| `duration_weeks` | BIGINT | Yes | NULL |  | Duration Weeks |
| `price_inr` | BIGINT | Yes | NULL |  | Price |
| `discount_price_inr` | BIGINT | Yes | NULL |  | Price |
| `language` | TEXT | Yes | NULL |  | Language |
| `rating` | FLOAT | Yes | NULL |  | Rating |
| `total_enrollments` | BIGINT | Yes | NULL |  | Total Enrollments |
| `course_format` | TEXT | Yes | NULL |  | Course Format |
| `certification` | TEXT | Yes | NULL |  | Certification |
| `placement_assistance` | TEXT | Yes | NULL |  | Placement Assistance |
| `launch_date` | DATETIME | Yes | NULL |  | Date |
| `status` | TEXT | Yes | NULL |  | Current status |
| `prerequisites` | TEXT | Yes | NULL |  | Prerequisites |
| `total_videos` | BIGINT | Yes | NULL |  | Unique identifier |
| `total_hours` | BIGINT | Yes | NULL |  | Total Hours |
| `includes_projects` | TEXT | Yes | NULL |  | Includes Projects |

**Sample Data:**
```
course_id | course_name | category | instructor_id | difficulty_level
-------------------------------------------------------------------------------
CRS00001 | UI/UX Design - Advan | Data Science | INS00112 | Beginner
CRS00002 | Cloud Computing - Ze | Mobile Development | INS00079 | Advanced
CRS00003 | Blockchain - Masterc | Full Stack Developme | INS00033 | Beginner

... and 15 more columns
```

---

### <a id='discussion_forums'></a>Discussion Forums

**Description:** No description available.

**Row Count:** 290

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `post_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `title` | TEXT | Yes | NULL |  | Title |
| `content` | TEXT | Yes | NULL |  | Content |
| `post_date` | DATETIME | Yes | NULL |  | Date |
| `category` | TEXT | Yes | NULL |  | Category |
| `upvotes` | BIGINT | Yes | NULL |  | Upvotes |
| `reply_count` | BIGINT | Yes | NULL |  | Reply Count |
| `views_count` | BIGINT | Yes | NULL |  | Views Count |
| `is_resolved` | TEXT | Yes | NULL |  | Is Resolved |
| `instructor_replied` | TEXT | Yes | NULL |  | Instructor Replied |
| `tags` | TEXT | Yes | NULL |  | Tags |
| `pinned` | TEXT | Yes | NULL |  | Pinned |
| `last_activity_date` | DATETIME | Yes | NULL |  | Date |

**Sample Data:**
```
post_id | course_id | student_id | title | content
------------------------------------------------------------
POST000001 | CRS00131 | STU000146 | Consectetur sunt vol | Aspernatur quasi mol
POST000002 | CRS00079 | STU000070 | Exercitationem fugia | Quibusdam unde volup
POST000003 | CRS00126 | STU000297 | Modi inventore rem s | Ipsam dolor pariatur

... and 10 more columns
```

---

### <a id='enrollments'></a>Enrollments

**Description:** No description available.

**Row Count:** 280

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `enrollment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `enrollment_date` | DATETIME | Yes | NULL |  | Date |
| `completion_date` | DATETIME | Yes | NULL |  | Date |
| `progress_percentage` | BIGINT | Yes | NULL |  | Progress Percentage |
| `status` | TEXT | Yes | NULL |  | Current status |
| `payment_status` | TEXT | Yes | NULL |  | Current status |
| `amount_paid_inr` | BIGINT | Yes | NULL |  | Unique identifier |
| `discount_applied` | BIGINT | Yes | NULL |  | Discount Applied |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |
| `certificate_issued` | TEXT | Yes | NULL |  | Certificate Issued |
| `final_grade` | FLOAT | Yes | NULL |  | Final Grade |
| `attendance_percentage` | FLOAT | Yes | NULL |  | Attendance Percentage |
| `feedback_rating` | FLOAT | Yes | NULL |  | Feedback Rating |

**Sample Data:**
```
enrollment_id | student_id | course_id | enrollment_date | completion_date
------------------------------------------------------------------------------------
ENR000001 | STU000007 | CRS00043 | 2025-10-23 00:00:00. | None
ENR000002 | STU000236 | CRS00174 | 2024-10-08 00:00:00. | None
ENR000003 | STU000033 | CRS00072 | 2024-07-29 00:00:00. | 2024-11-19 00:00:00.

... and 10 more columns
```

---

### <a id='instructors'></a>Instructors

**Description:** No description available.

**Row Count:** 250

**Column Count:** 19

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `instructor_id` | TEXT | Yes | NULL |  | Unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | BIGINT | Yes | NULL |  | Phone number |
| `specialization` | TEXT | Yes | NULL |  | Specialization |
| `years_of_experience` | BIGINT | Yes | NULL |  | Years Of Experience |
| `education_level` | TEXT | Yes | NULL |  | Education Level |
| `rating` | FLOAT | Yes | NULL |  | Rating |
| `total_students_taught` | BIGINT | Yes | NULL |  | Total Students Taught |
| `total_courses` | BIGINT | Yes | NULL |  | Total Courses |
| `join_date` | DATETIME | Yes | NULL |  | Date |
| `city` | TEXT | Yes | NULL |  | City name |
| `linkedin_profile` | TEXT | Yes | NULL |  | Linkedin Profile |
| `hourly_rate_inr` | BIGINT | Yes | NULL |  | Hourly Rate Inr |
| `employment_type` | TEXT | Yes | NULL |  | Employment Type |
| `status` | TEXT | Yes | NULL |  | Current status |
| `bio` | TEXT | Yes | NULL |  | Bio |
| `languages_spoken` | TEXT | Yes | NULL |  | Languages Spoken |

**Sample Data:**
```
instructor_id | first_name | last_name | email | phone
----------------------------------------------------------------
INS00001 | Ishita | Sharaf | pbansal@example.net | 919232642418
INS00002 | Samaira | Shenoy | takkeya@example.org | 918590882657
INS00003 | Uthkarsh | Manda | suripihu@example.org | 918517490023

... and 14 more columns
```

---

### <a id='live_classes'></a>Live Classes

**Description:** No description available.

**Row Count:** 240

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `class_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `instructor_id` | TEXT | Yes | NULL |  | Unique identifier |
| `title` | TEXT | Yes | NULL |  | Title |
| `scheduled_date` | DATETIME | Yes | NULL |  | Date |
| `duration_minutes` | BIGINT | Yes | NULL |  | Duration Minutes |
| `meeting_link` | TEXT | Yes | NULL |  | Meeting Link |
| `recording_url` | TEXT | Yes | NULL |  | Recording Url |
| `attendees_count` | BIGINT | Yes | NULL |  | Attendees Count |
| `max_capacity` | BIGINT | Yes | NULL |  | City name |
| `status` | TEXT | Yes | NULL |  | Current status |
| `platform` | TEXT | Yes | NULL |  | Platform |
| `chat_transcript_url` | TEXT | Yes | NULL |  | Chat Transcript Url |
| `poll_conducted` | TEXT | Yes | NULL |  | Poll Conducted |
| `avg_rating` | FLOAT | Yes | NULL |  | Avg Rating |

**Sample Data:**
```
class_id | course_id | instructor_id | title | scheduled_date
-----------------------------------------------------------------------
CLS000001 | CRS00137 | INS00067 | Realigned leadingedg | 2025-10-11 00:00:00.
CLS000002 | CRS00116 | INS00175 | Team-oriented transi | 2024-12-12 00:00:00.
CLS000003 | CRS00185 | INS00014 | Networked foreground | 2025-03-15 00:00:00.

... and 10 more columns
```

---

### <a id='mentorship'></a>Mentorship

**Description:** No description available.

**Row Count:** 245

**Column Count:** 14

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `session_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `mentor_id` | TEXT | Yes | NULL |  | Unique identifier |
| `session_date` | DATETIME | Yes | NULL |  | Date |
| `duration_minutes` | BIGINT | Yes | NULL |  | Duration Minutes |
| `session_type` | TEXT | Yes | NULL |  | Session Type |
| `meeting_platform` | TEXT | Yes | NULL |  | Meeting Platform |
| `status` | TEXT | Yes | NULL |  | Current status |
| `student_rating` | FLOAT | Yes | NULL |  | Student Rating |
| `feedback` | TEXT | Yes | NULL |  | Feedback |
| `topics_discussed` | TEXT | Yes | NULL |  | Topics Discussed |
| `action_items` | TEXT | Yes | NULL |  | Action Items |
| `follow_up_required` | TEXT | Yes | NULL |  | Follow Up Required |
| `recording_url` | TEXT | Yes | NULL |  | Recording Url |

**Sample Data:**
```
session_id | student_id | mentor_id | session_date | duration_minutes
-------------------------------------------------------------------------------
MNT000001 | STU000124 | INS00229 | 2025-03-23 00:00:00. | 60
MNT000002 | STU000087 | INS00011 | 2025-05-19 00:00:00. | 45
MNT000003 | STU000139 | INS00177 | 2025-08-06 00:00:00. | 60

... and 9 more columns
```

---

### <a id='partnerships'></a>Partnerships

**Description:** No description available.

**Row Count:** 215

**Column Count:** 16

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `partnership_id` | TEXT | Yes | NULL |  | Unique identifier |
| `company_name` | TEXT | Yes | NULL |  | Name |
| `company_type` | TEXT | Yes | NULL |  | Company Type |
| `partnership_type` | TEXT | Yes | NULL |  | Partnership Type |
| `start_date` | DATETIME | Yes | NULL |  | Date |
| `contract_value_lakhs` | FLOAT | Yes | NULL |  | Contract Value Lakhs |
| `employees_trained` | BIGINT | Yes | NULL |  | Employees Trained |
| `courses_subscribed` | BIGINT | Yes | NULL |  | Courses Subscribed |
| `status` | TEXT | Yes | NULL |  | Current status |
| `point_of_contact` | TEXT | Yes | NULL |  | Point Of Contact |
| `contact_email` | TEXT | Yes | NULL |  | Email address |
| `contact_phone` | BIGINT | Yes | NULL |  | Phone number |
| `city` | TEXT | Yes | NULL |  | City name |
| `renewal_date` | DATETIME | Yes | NULL |  | Date |
| `placements_provided` | BIGINT | Yes | NULL |  | Unique identifier |
| `discount_percentage` | BIGINT | Yes | NULL |  | Discount Percentage |

**Sample Data:**
```
partnership_id | company_name | company_type | partnership_type | start_date
--------------------------------------------------------------------------------------
PRT00001 | Dora, Chadha and Sha | Product Company | Corporate Training | 2023-10-20 00:00:00.
PRT00002 | Ahuja, Sani and Sach | Consulting | Placement Partner | 2023-11-13 00:00:00.
PRT00003 | Goda, Banik and Srin | Product Company | Technology Partner | 2024-02-08 00:00:00.

... and 11 more columns
```

---

### <a id='payments'></a>Payments

**Description:** No description available.

**Row Count:** 270

**Column Count:** 16

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `payment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `enrollment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `amount_inr` | BIGINT | Yes | NULL |  | Amount Inr |
| `payment_method` | TEXT | Yes | NULL |  | Payment Method |
| `payment_status` | TEXT | Yes | NULL |  | Current status |
| `transaction_id` | TEXT | Yes | NULL |  | Unique identifier |
| `payment_date` | DATETIME | Yes | NULL |  | Date |
| `payment_gateway` | TEXT | Yes | NULL |  | Payment Gateway |
| `discount_code` | TEXT | Yes | NULL |  | Discount Code |
| `discount_amount_inr` | FLOAT | Yes | NULL |  | Discount Amount Inr |
| `gst_amount_inr` | FLOAT | Yes | NULL |  | Gst Amount Inr |
| `net_amount_inr` | FLOAT | Yes | NULL |  | Net Amount Inr |
| `refund_status` | TEXT | Yes | NULL |  | Current status |
| `invoice_number` | TEXT | Yes | NULL |  | Invoice Number |
| `emi_opted` | TEXT | Yes | NULL |  | Emi Opted |

**Sample Data:**
```
payment_id | student_id | enrollment_id | amount_inr | payment_method
-------------------------------------------------------------------------------
PAY000001 | STU000222 | ENR000219 | 12707 | Net Banking
PAY000002 | STU000211 | ENR000273 | 6020 | Credit Card
PAY000003 | STU000017 | ENR000167 | 113942 | PhonePe

... and 11 more columns
```

---

### <a id='placements'></a>Placements

**Description:** No description available.

**Row Count:** 210

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `placement_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `company_name` | TEXT | Yes | NULL |  | Name |
| `job_title` | TEXT | Yes | NULL |  | Job Title |
| `ctc_lakhs` | FLOAT | Yes | NULL |  | Ctc Lakhs |
| `placement_date` | DATETIME | Yes | NULL |  | Date |
| `job_location` | TEXT | Yes | NULL |  | Job Location |
| `job_type` | TEXT | Yes | NULL |  | Job Type |
| `course_completed` | TEXT | Yes | NULL |  | Course Completed |
| `company_tier` | TEXT | Yes | NULL |  | Company Tier |
| `referral_bonus_given` | TEXT | Yes | NULL |  | Referral Bonus Given |
| `employment_status` | TEXT | Yes | NULL |  | Current status |
| `interview_rounds` | BIGINT | Yes | NULL |  | Interview Rounds |
| `offer_letter_date` | DATETIME | Yes | NULL |  | Date |
| `stipend_inr` | FLOAT | Yes | NULL |  | Stipend Inr |

**Sample Data:**
```
placement_id | student_id | company_name | job_title | ctc_lakhs
--------------------------------------------------------------------------
PLC000001 | STU000030 | Bera-Sathe | Software Engineer | 29.95
PLC000002 | STU000248 | Dhar LLC | DevOps Engineer | 39.06
PLC000003 | STU000223 | Dubey-Chatterjee | Full Stack Developer | 3.57

... and 10 more columns
```

---

### <a id='student_progress'></a>Student Progress

**Description:** No description available.

**Row Count:** 285

**Column Count:** 18

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `progress_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `course_id` | TEXT | Yes | NULL |  | Unique identifier |
| `videos_completed` | BIGINT | Yes | NULL |  | Unique identifier |
| `total_videos` | BIGINT | Yes | NULL |  | Unique identifier |
| `quizzes_completed` | BIGINT | Yes | NULL |  | Quizzes Completed |
| `total_quizzes` | BIGINT | Yes | NULL |  | Total Quizzes |
| `assignments_submitted` | BIGINT | Yes | NULL |  | Assignments Submitted |
| `total_assignments` | BIGINT | Yes | NULL |  | Total Assignments |
| `progress_percentage` | FLOAT | Yes | NULL |  | Progress Percentage |
| `time_spent_hours` | FLOAT | Yes | NULL |  | Time Spent Hours |
| `last_accessed_date` | DATETIME | Yes | NULL |  | Date |
| `streak_days` | BIGINT | Yes | NULL |  | Streak Days |
| `certificates_earned` | BIGINT | Yes | NULL |  | Certificates Earned |
| `skill_badges_earned` | BIGINT | Yes | NULL |  | Skill Badges Earned |
| `current_module` | BIGINT | Yes | NULL |  | Current Module |
| `estimated_completion_date` | DATETIME | Yes | NULL |  | Date |
| `daily_avg_time_minutes` | BIGINT | Yes | NULL |  | Daily Avg Time Minutes |

**Sample Data:**
```
progress_id | student_id | course_id | videos_completed | total_videos
--------------------------------------------------------------------------------
PRG000001 | STU000134 | CRS00129 | 116 | 129
PRG000002 | STU000238 | CRS00108 | 35 | 164
PRG000003 | STU000041 | CRS00063 | 64 | 119

... and 13 more columns
```

---

### <a id='students'></a>Students

**Description:** No description available.

**Row Count:** 300

**Column Count:** 20

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `first_name` | TEXT | Yes | NULL |  | First name |
| `last_name` | TEXT | Yes | NULL |  | Last name |
| `email` | TEXT | Yes | NULL |  | Email address |
| `phone` | BIGINT | Yes | NULL |  | Phone number |
| `date_of_birth` | DATETIME | Yes | NULL |  | Date |
| `gender` | TEXT | Yes | NULL |  | Gender |
| `city` | TEXT | Yes | NULL |  | City name |
| `state` | TEXT | Yes | NULL |  | State code |
| `current_education` | TEXT | Yes | NULL |  | Current Education |
| `college_name` | TEXT | Yes | NULL |  | Name |
| `enrollment_date` | DATETIME | Yes | NULL |  | Date |
| `account_status` | TEXT | Yes | NULL |  | Current status |
| `referral_code` | TEXT | Yes | NULL |  | Referral Code |
| `linkedin_profile` | TEXT | Yes | NULL |  | Linkedin Profile |
| `github_profile` | TEXT | Yes | NULL |  | Github Profile |
| `career_goal` | TEXT | Yes | NULL |  | Career Goal |
| `previous_experience_years` | BIGINT | Yes | NULL |  | Previous Experience Years |
| `preferred_language` | TEXT | Yes | NULL |  | Preferred Language |
| `subscription_tier` | TEXT | Yes | NULL |  | Subscription Tier |

**Sample Data:**
```
student_id | first_name | last_name | email | phone
-------------------------------------------------------------
STU000001 | Navya | Devi | kartikamble@example. | 918649969065
STU000002 | Heer | Tandon | ybandi@example.net | 918071379473
STU000003 | Stuvan | Venkatesh | lhayer@example.net | 919958195784

... and 15 more columns
```

---

### <a id='submissions'></a>Submissions

**Description:** No description available.

**Row Count:** 260

**Column Count:** 15

| Column Name | Data Type | Nullable | Default | Primary Key | Description |
|-------------|-----------|----------|---------|-------------|-------------|
| `submission_id` | TEXT | Yes | NULL |  | Unique identifier |
| `assessment_id` | TEXT | Yes | NULL |  | Unique identifier |
| `student_id` | TEXT | Yes | NULL |  | Unique identifier |
| `submitted_date` | DATETIME | Yes | NULL |  | Date |
| `graded_date` | DATETIME | Yes | NULL |  | Date |
| `score_obtained` | FLOAT | Yes | NULL |  | Score Obtained |
| `max_score` | BIGINT | Yes | NULL |  | Max Score |
| `grade` | TEXT | Yes | NULL |  | Grade |
| `attempt_number` | BIGINT | Yes | NULL |  | Attempt Number |
| `time_taken_minutes` | BIGINT | Yes | NULL |  | Time Taken Minutes |
| `status` | TEXT | Yes | NULL |  | Current status |
| `feedback` | TEXT | Yes | NULL |  | Feedback |
| `plagiarism_score` | FLOAT | Yes | NULL |  | Plagiarism Score |
| `submission_url` | TEXT | Yes | NULL |  | Submission Url |
| `late_submission` | TEXT | Yes | NULL |  | Late Submission |

**Sample Data:**
```
submission_id | assessment_id | student_id | submitted_date | graded_date
-----------------------------------------------------------------------------------
SUB000001 | ASM000025 | STU000100 | 2025-01-02 00:00:00. | 2025-01-03 00:00:00.
SUB000002 | ASM000151 | STU000231 | 2024-02-26 00:00:00. | 2024-02-29 00:00:00.
SUB000003 | ASM000066 | STU000076 | 2025-07-09 00:00:00. | 2025-07-13 00:00:00.

... and 10 more columns
```

---

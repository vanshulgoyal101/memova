"""
Excel Data Generator for EdTech Company (India)
Generates 15 realistic Excel files with 200-300 rows and 10-20 columns each
Represents a comprehensive Indian EdTech platform
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

from src.utils.config import Config

# Initialize Faker with India locale
fake = Faker(['en_IN'])
Faker.seed(200)
random.seed(200)

# Output directory
config = Config()
OUTPUT_DIR = os.path.join(config.EXCEL_OUTPUT_DIR, 'edtech_company')


# Indian-specific data
INDIAN_CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore', 'Bhopal', 'Nagpur']
INDIAN_STATES = ['Maharashtra', 'Delhi', 'Karnataka', 'Telangana', 'Tamil Nadu', 'West Bengal', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Punjab', 'Kerala', 'Madhya Pradesh']
COURSE_CATEGORIES = ['Data Science', 'Web Development', 'Mobile Development', 'DevOps', 'Cloud Computing', 'AI/ML', 'Cybersecurity', 'Blockchain', 'Full Stack Development', 'UI/UX Design']
EDUCATION_LEVELS = ['10th', '12th', 'Bachelors', 'Masters', 'PhD']
COLLEGES = ['IIT Delhi', 'IIT Bombay', 'IIT Madras', 'BITS Pilani', 'NIT Trichy', 'IIIT Hyderabad', 'VIT Vellore', 'Delhi University', 'Mumbai University', 'Anna University']


def generate_students(num_rows=300):
    """Generate student enrollment data"""
    data = []
    for i in range(num_rows):
        enrollment_date = fake.date_between(start_date='-3y', end_date='today')
        
        data.append({
            'student_id': f'STU{str(i+1).zfill(6)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': f'+91{random.randint(7000000000, 9999999999)}',
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=35),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'city': random.choice(INDIAN_CITIES),
            'state': random.choice(INDIAN_STATES),
            'current_education': random.choice(EDUCATION_LEVELS),
            'college_name': random.choice(COLLEGES),
            'enrollment_date': enrollment_date,
            'account_status': random.choice(['Active', 'Active', 'Active', 'Inactive', 'Suspended']),
            'referral_code': f'REF{random.randint(1000, 9999)}' if random.random() > 0.7 else None,
            'linkedin_profile': f'linkedin.com/in/{fake.user_name()}' if random.random() > 0.5 else None,
            'github_profile': f'github.com/{fake.user_name()}' if random.random() > 0.6 else None,
            'career_goal': random.choice(['Software Engineer', 'Data Scientist', 'DevOps Engineer', 'Product Manager', 'Full Stack Developer', 'ML Engineer']),
            'previous_experience_years': random.choice([0, 0, 1, 2, 3, 4, 5]),
            'preferred_language': random.choice(['English', 'Hindi', 'English+Hindi']),
            'subscription_tier': random.choice(['Free', 'Premium', 'Pro', 'Enterprise'])
        })
    
    df = pd.DataFrame(data)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, 'students.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_instructors(num_rows=250):
    """Generate instructor data"""
    data = []
    for i in range(num_rows):
        join_date = fake.date_between(start_date='-5y', end_date='-6m')
        
        data.append({
            'instructor_id': f'INS{str(i+1).zfill(5)}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': f'+91{random.randint(7000000000, 9999999999)}',
            'specialization': random.choice(COURSE_CATEGORIES),
            'years_of_experience': random.randint(2, 20),
            'education_level': random.choice(['Bachelors', 'Masters', 'PhD']),
            'rating': round(random.uniform(3.5, 5.0), 2),
            'total_students_taught': random.randint(100, 10000),
            'total_courses': random.randint(1, 15),
            'join_date': join_date,
            'city': random.choice(INDIAN_CITIES),
            'linkedin_profile': f'linkedin.com/in/{fake.user_name()}',
            'hourly_rate_inr': random.randint(500, 5000),
            'employment_type': random.choice(['Full-time', 'Part-time', 'Freelance']),
            'status': random.choice(['Active', 'Active', 'Active', 'On Leave']),
            'bio': fake.text(max_nb_chars=200),
            'languages_spoken': random.choice(['English', 'Hindi', 'English+Hindi', 'English+Tamil', 'English+Telugu'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'instructors.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_courses(num_rows=200):
    """Generate course catalog"""
    data = []
    for i in range(num_rows):
        duration_weeks = random.choice([4, 6, 8, 12, 16, 24])
        price = random.randint(5000, 150000)
        
        data.append({
            'course_id': f'CRS{str(i+1).zfill(5)}',
            'course_name': f'{random.choice(COURSE_CATEGORIES)} - {random.choice(["Bootcamp", "Masterclass", "Complete Guide", "Zero to Hero", "Advanced Track"])}',
            'category': random.choice(COURSE_CATEGORIES),
            'instructor_id': f'INS{str(random.randint(1, 250)).zfill(5)}',
            'difficulty_level': random.choice(['Beginner', 'Intermediate', 'Advanced']),
            'duration_weeks': duration_weeks,
            'price_inr': price,
            'discount_price_inr': int(price * random.choice([0.7, 0.8, 0.9, 1.0])),
            'language': random.choice(['English', 'Hindi', 'English+Hindi']),
            'rating': round(random.uniform(3.0, 5.0), 2),
            'total_enrollments': random.randint(50, 5000),
            'course_format': random.choice(['Self-paced', 'Live Classes', 'Hybrid']),
            'certification': random.choice(['Yes', 'Yes', 'No']),
            'placement_assistance': random.choice(['Yes', 'No']),
            'launch_date': fake.date_between(start_date='-3y', end_date='today'),
            'status': random.choice(['Active', 'Active', 'Active', 'Archived']),
            'prerequisites': random.choice(['None', 'Basic Programming', 'Intermediate Python', 'Advanced Algorithms']),
            'total_videos': random.randint(20, 200),
            'total_hours': random.randint(10, 150),
            'includes_projects': random.choice(['Yes', 'Yes', 'No'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'courses.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_enrollments(num_rows=280):
    """Generate student course enrollments"""
    data = []
    for i in range(num_rows):
        enrollment_date = fake.date_between(start_date='-2y', end_date='today')
        completion_date = enrollment_date + timedelta(days=random.randint(30, 180)) if random.random() > 0.4 else None
        
        data.append({
            'enrollment_id': f'ENR{str(i+1).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'enrollment_date': enrollment_date,
            'completion_date': completion_date,
            'progress_percentage': random.randint(0, 100) if not completion_date else 100,
            'status': random.choice(['In Progress', 'Completed', 'Dropped', 'In Progress', 'In Progress']),
            'payment_status': random.choice(['Paid', 'Paid', 'Pending', 'Refunded']),
            'amount_paid_inr': random.randint(5000, 150000),
            'discount_applied': random.choice([0, 10, 20, 30, 50]),
            'payment_method': random.choice(['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'EMI']),
            'certificate_issued': 'Yes' if completion_date else 'No',
            'final_grade': round(random.uniform(60, 100), 2) if completion_date else None,
            'attendance_percentage': round(random.uniform(50, 100), 2),
            'feedback_rating': round(random.uniform(3.0, 5.0), 2) if completion_date else None
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'enrollments.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_course_content(num_rows=250):
    """Generate course content modules and lectures"""
    data = []
    for i in range(num_rows):
        data.append({
            'content_id': f'CNT{str(i+1).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'module_number': random.randint(1, 10),
            'lecture_number': random.randint(1, 20),
            'title': f'{random.choice(["Introduction to", "Deep Dive into", "Advanced", "Practical", "Hands-on"])} {fake.bs()}',
            'content_type': random.choice(['Video', 'Reading', 'Quiz', 'Coding Exercise', 'Project']),
            'duration_minutes': random.randint(5, 120),
            'is_free_preview': random.choice(['Yes', 'No', 'No', 'No']),
            'order_index': i,
            'upload_date': fake.date_between(start_date='-3y', end_date='today'),
            'views_count': random.randint(50, 10000),
            'avg_completion_time_minutes': random.randint(5, 150),
            'difficulty': random.choice(['Easy', 'Medium', 'Hard']),
            'resources_url': f'https://resources.edtech.com/{fake.uuid4()}',
            'transcript_available': random.choice(['Yes', 'No'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'course_content.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_assessments(num_rows=220):
    """Generate assessments and quizzes"""
    data = []
    for i in range(num_rows):
        data.append({
            'assessment_id': f'ASM{str(i+1).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'assessment_type': random.choice(['Quiz', 'Coding Challenge', 'Project', 'MCQ Test', 'Assignment']),
            'title': f'{fake.catch_phrase()} Assessment',
            'max_score': random.choice([10, 20, 50, 100]),
            'passing_score': random.choice([40, 50, 60, 70]),
            'duration_minutes': random.randint(15, 180),
            'total_questions': random.randint(5, 50),
            'difficulty': random.choice(['Easy', 'Medium', 'Hard']),
            'is_proctored': random.choice(['Yes', 'No', 'No']),
            'attempts_allowed': random.randint(1, 3),
            'created_date': fake.date_between(start_date='-3y', end_date='today'),
            'status': random.choice(['Active', 'Active', 'Draft', 'Archived']),
            'weightage_percentage': random.randint(5, 30)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'assessments.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_submissions(num_rows=260):
    """Generate student assessment submissions"""
    data = []
    for i in range(num_rows):
        submitted_date = fake.date_between(start_date='-2y', end_date='today')
        graded_date = submitted_date + timedelta(days=random.randint(1, 7)) if random.random() > 0.2 else None
        
        data.append({
            'submission_id': f'SUB{str(i+1).zfill(6)}',
            'assessment_id': f'ASM{str(random.randint(1, 220)).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'submitted_date': submitted_date,
            'graded_date': graded_date,
            'score_obtained': random.randint(0, 100) if graded_date else None,
            'max_score': 100,
            'grade': random.choice(['A+', 'A', 'B+', 'B', 'C', 'D', 'F']) if graded_date else None,
            'attempt_number': random.randint(1, 3),
            'time_taken_minutes': random.randint(15, 180),
            'status': random.choice(['Graded', 'Pending', 'Graded', 'Graded']),
            'feedback': fake.text(max_nb_chars=150) if graded_date else None,
            'plagiarism_score': round(random.uniform(0, 15), 2),
            'submission_url': f'https://submissions.edtech.com/{fake.uuid4()}',
            'late_submission': random.choice(['Yes', 'No', 'No', 'No'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'submissions.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_payments(num_rows=270):
    """Generate payment transactions"""
    data = []
    for i in range(num_rows):
        amount = random.randint(5000, 150000)
        
        data.append({
            'payment_id': f'PAY{str(i+1).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'enrollment_id': f'ENR{str(random.randint(1, 280)).zfill(6)}',
            'amount_inr': amount,
            'payment_method': random.choice(['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Paytm', 'PhonePe', 'Google Pay']),
            'payment_status': random.choice(['Success', 'Success', 'Success', 'Failed', 'Pending']),
            'transaction_id': f'TXN{fake.uuid4()[:12].upper()}',
            'payment_date': fake.date_between(start_date='-2y', end_date='today'),
            'payment_gateway': random.choice(['Razorpay', 'Paytm', 'PayU', 'CCAvenue', 'Instamojo']),
            'discount_code': f'DISC{random.randint(10, 99)}' if random.random() > 0.7 else None,
            'discount_amount_inr': amount * random.choice([0, 0.1, 0.2, 0.3]),
            'gst_amount_inr': amount * 0.18,
            'net_amount_inr': amount * 1.18,
            'refund_status': random.choice(['No Refund', 'No Refund', 'Partial', 'Full']) if random.random() > 0.9 else 'No Refund',
            'invoice_number': f'INV{str(i+1).zfill(6)}',
            'emi_opted': random.choice(['Yes', 'No', 'No', 'No'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'payments.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_certificates(num_rows=230):
    """Generate course completion certificates"""
    data = []
    for i in range(num_rows):
        issue_date = fake.date_between(start_date='-2y', end_date='today')
        
        data.append({
            'certificate_id': f'CERT{str(i+1).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'enrollment_id': f'ENR{str(random.randint(1, 280)).zfill(6)}',
            'issue_date': issue_date,
            'certificate_url': f'https://certificates.edtech.com/{fake.uuid4()}',
            'verification_code': f'VER{fake.uuid4()[:8].upper()}',
            'final_grade': round(random.uniform(70, 100), 2),
            'rank_in_batch': random.randint(1, 100),
            'total_batch_size': random.randint(50, 500),
            'skills_earned': ', '.join(random.sample(['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker', 'Kubernetes', 'MongoDB'], random.randint(3, 6))),
            'credential_id': f'CRED{fake.uuid4()[:10].upper()}',
            'blockchain_verified': random.choice(['Yes', 'No', 'No'])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'certificates.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_live_classes(num_rows=240):
    """Generate live class sessions"""
    data = []
    for i in range(num_rows):
        scheduled_date = fake.date_between(start_date='-1y', end_date='+3m')
        
        data.append({
            'class_id': f'CLS{str(i+1).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'instructor_id': f'INS{str(random.randint(1, 250)).zfill(5)}',
            'title': f'{fake.catch_phrase()} - Live Session',
            'scheduled_date': scheduled_date,
            'duration_minutes': random.choice([60, 90, 120, 180]),
            'meeting_link': f'https://zoom.us/j/{random.randint(100000000, 999999999)}',
            'recording_url': f'https://recordings.edtech.com/{fake.uuid4()}' if random.random() > 0.3 else None,
            'attendees_count': random.randint(10, 500),
            'max_capacity': random.choice([50, 100, 200, 500, 1000]),
            'status': random.choice(['Completed', 'Scheduled', 'Cancelled', 'Completed', 'Completed']),
            'platform': random.choice(['Zoom', 'Google Meet', 'Microsoft Teams']),
            'chat_transcript_url': f'https://transcripts.edtech.com/{fake.uuid4()}' if random.random() > 0.5 else None,
            'poll_conducted': random.choice(['Yes', 'No']),
            'avg_rating': round(random.uniform(3.5, 5.0), 2)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'live_classes.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_discussion_forums(num_rows=290):
    """Generate discussion forum posts"""
    data = []
    for i in range(num_rows):
        post_date = fake.date_between(start_date='-2y', end_date='today')
        
        data.append({
            'post_id': f'POST{str(i+1).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'title': fake.sentence(nb_words=6),
            'content': fake.text(max_nb_chars=300),
            'post_date': post_date,
            'category': random.choice(['Doubt', 'Discussion', 'Resource Share', 'Career Advice', 'Project Help']),
            'upvotes': random.randint(0, 500),
            'reply_count': random.randint(0, 50),
            'views_count': random.randint(10, 5000),
            'is_resolved': random.choice(['Yes', 'No', 'No']),
            'instructor_replied': random.choice(['Yes', 'No', 'No']),
            'tags': ', '.join(random.sample(['python', 'javascript', 'aws', 'docker', 'react', 'sql', 'api', 'debugging'], random.randint(2, 5))),
            'pinned': random.choice(['Yes', 'No', 'No', 'No']),
            'last_activity_date': post_date + timedelta(days=random.randint(0, 30))
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'discussion_forums.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_student_progress(num_rows=285):
    """Generate student progress tracking"""
    data = []
    for i in range(num_rows):
        data.append({
            'progress_id': f'PRG{str(i+1).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'course_id': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'videos_completed': random.randint(0, 200),
            'total_videos': random.randint(100, 200),
            'quizzes_completed': random.randint(0, 50),
            'total_quizzes': random.randint(20, 50),
            'assignments_submitted': random.randint(0, 20),
            'total_assignments': random.randint(10, 20),
            'progress_percentage': round(random.uniform(0, 100), 2),
            'time_spent_hours': round(random.uniform(5, 300), 2),
            'last_accessed_date': fake.date_between(start_date='-1m', end_date='today'),
            'streak_days': random.randint(0, 365),
            'certificates_earned': random.randint(0, 5),
            'skill_badges_earned': random.randint(0, 15),
            'current_module': random.randint(1, 10),
            'estimated_completion_date': fake.date_between(start_date='today', end_date='+6m'),
            'daily_avg_time_minutes': random.randint(15, 180)
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'student_progress.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_placements(num_rows=210):
    """Generate placement and job placement records"""
    data = []
    for i in range(num_rows):
        placement_date = fake.date_between(start_date='-2y', end_date='today')
        
        data.append({
            'placement_id': f'PLC{str(i+1).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'company_name': fake.company(),
            'job_title': random.choice(['Software Engineer', 'Data Analyst', 'Full Stack Developer', 'DevOps Engineer', 'ML Engineer', 'Frontend Developer', 'Backend Developer']),
            'ctc_lakhs': round(random.uniform(3.0, 45.0), 2),
            'placement_date': placement_date,
            'job_location': random.choice(INDIAN_CITIES),
            'job_type': random.choice(['Full-time', 'Internship', 'Contract']),
            'course_completed': f'CRS{str(random.randint(1, 200)).zfill(5)}',
            'company_tier': random.choice(['Product', 'Service', 'Startup', 'MNC']),
            'referral_bonus_given': random.choice(['Yes', 'No', 'No']),
            'employment_status': random.choice(['Joined', 'Offer Accepted', 'Offer Pending']),
            'interview_rounds': random.randint(2, 6),
            'offer_letter_date': placement_date - timedelta(days=random.randint(7, 30)),
            'stipend_inr': random.randint(10000, 50000) if random.random() > 0.5 else None
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'placements.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_mentorship(num_rows=245):
    """Generate mentorship sessions"""
    data = []
    for i in range(num_rows):
        session_date = fake.date_between(start_date='-1y', end_date='today')
        
        data.append({
            'session_id': f'MNT{str(i+1).zfill(6)}',
            'student_id': f'STU{str(random.randint(1, 300)).zfill(6)}',
            'mentor_id': f'INS{str(random.randint(1, 250)).zfill(5)}',
            'session_date': session_date,
            'duration_minutes': random.choice([30, 45, 60, 90]),
            'session_type': random.choice(['Career Guidance', 'Technical Doubt', 'Project Review', 'Mock Interview', 'Resume Review']),
            'meeting_platform': random.choice(['Zoom', 'Google Meet', 'Phone Call']),
            'status': random.choice(['Completed', 'Scheduled', 'Cancelled', 'Completed', 'Completed']),
            'student_rating': round(random.uniform(3.5, 5.0), 2) if random.random() > 0.3 else None,
            'feedback': fake.text(max_nb_chars=150) if random.random() > 0.4 else None,
            'topics_discussed': ', '.join(random.sample(['Career', 'DSA', 'System Design', 'Projects', 'Interview Prep', 'Resume'], random.randint(2, 4))),
            'action_items': fake.sentence(nb_words=10),
            'follow_up_required': random.choice(['Yes', 'No', 'No']),
            'recording_url': f'https://mentorship-recordings.edtech.com/{fake.uuid4()}' if random.random() > 0.6 else None
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'mentorship.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_partnerships(num_rows=215):
    """Generate corporate partnerships and B2B relationships"""
    data = []
    for i in range(num_rows):
        partnership_date = fake.date_between(start_date='-3y', end_date='today')
        
        data.append({
            'partnership_id': f'PRT{str(i+1).zfill(5)}',
            'company_name': fake.company(),
            'company_type': random.choice(['Tech Startup', 'IT Services', 'Product Company', 'Consulting', 'E-commerce']),
            'partnership_type': random.choice(['Placement Partner', 'Corporate Training', 'Hiring Partner', 'Technology Partner']),
            'start_date': partnership_date,
            'contract_value_lakhs': round(random.uniform(5.0, 500.0), 2),
            'employees_trained': random.randint(10, 1000),
            'courses_subscribed': random.randint(1, 20),
            'status': random.choice(['Active', 'Active', 'Active', 'Expired', 'Paused']),
            'point_of_contact': fake.name(),
            'contact_email': fake.company_email(),
            'contact_phone': f'+91{random.randint(7000000000, 9999999999)}',
            'city': random.choice(INDIAN_CITIES),
            'renewal_date': partnership_date + timedelta(days=365) if random.random() > 0.3 else None,
            'placements_provided': random.randint(0, 100),
            'discount_percentage': random.choice([10, 15, 20, 25, 30])
        })
    
    df = pd.DataFrame(data)
    filepath = os.path.join(OUTPUT_DIR, 'partnerships.xlsx')
    df.to_excel(filepath, index=False)
    print(f"✅ Generated: {filepath} ({num_rows} rows, {len(df.columns)} columns)")
    return df


def generate_all_edtech_data():
    """Generate all EdTech company Excel files"""
    print("\n" + "=" * 70)
    print("  📚 EDTECH INDIA - DATA GENERATION")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate all datasets
    datasets = {
        'students': generate_students(300),
        'instructors': generate_instructors(250),
        'courses': generate_courses(200),
        'enrollments': generate_enrollments(280),
        'course_content': generate_course_content(250),
        'assessments': generate_assessments(220),
        'submissions': generate_submissions(260),
        'payments': generate_payments(270),
        'certificates': generate_certificates(230),
        'live_classes': generate_live_classes(240),
        'discussion_forums': generate_discussion_forums(290),
        'student_progress': generate_student_progress(285),
        'placements': generate_placements(210),
        'mentorship': generate_mentorship(245),
        'partnerships': generate_partnerships(215)
    }
    
    total_rows = sum(len(df) for df in datasets.values())
    total_files = len(datasets)
    
    print("\n" + "=" * 70)
    print("  ✨ GENERATION COMPLETE!")
    print("=" * 70)
    print(f"  Total Files: {total_files}")
    print(f"  Total Rows: {total_rows}")
    print(f"  Output Directory: {OUTPUT_DIR}")
    print("=" * 70 + "\n")
    
    return datasets


if __name__ == "__main__":
    generate_all_edtech_data()

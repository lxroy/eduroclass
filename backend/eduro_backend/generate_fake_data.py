import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduro_backend.settings')
django.setup()


import random
from faker import Faker
from sms.models import School, Department, Teacher, Course, Student, Class, Attendance, Exam, Result


# faker.py


fake = Faker()

# Create schools
for _ in range(5):
    School.objects.create(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        is_school=True,
        name=fake.company(),
        address=fake.address(),
        school_type=random.choice(['public', 'private']),
        accreditation_status=fake.word(),
        founding_date=fake.date_this_decade(),
        principal_name=fake.name(),
        principal_email=fake.email(),
        principal_phone_number=fake.phone_number(),
    )

# Create departments
for _ in range(10):
    Department.objects.create(
        name=fake.word(),
        code=fake.word()[:5],
        description=fake.text(),
        school=random.choice(School.objects.all())
    )

# Create teachers
for _ in range(20):
    Teacher.objects.create(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        is_teacher=True,
        school=random.choice(School.objects.all()),
        profile_picture=fake.image_url(),
    )

# Create courses
for _ in range(15):
    Course.objects.create(
        name=fake.word(),
        code=fake.word()[:5],
        description=fake.text(),
        department=random.choice(Department.objects.all())
    )

# Create students
for _ in range(50):
    Student.objects.create(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        is_student=True,
        school=random.choice(School.objects.all()),
        profile_picture=fake.image_url(),
    )

# Create classes
for _ in range(8):
    Class.objects.create(
        name=fake.word(),
        description=fake.text(),
    )

# Create attendances
for _ in range(100):
    Attendance.objects.create(
        date=fake.date_this_year(),
        student=random.choice(Student.objects.all()),
        is_present=fake.boolean(),
        class_attended=random.choice(Class.objects.all()),
        school=random.choice(School.objects.all())
    )

# Create exams
for _ in range(30):
    Exam.objects.create(
        date=fake.date_this_year(),
        start_time=fake.time(),
        end_time=fake.time(),
        venue=fake.word(),
        course=random.choice(Course.objects.all()),
        class_examined=random.choice(Class.objects.all()),
        school=random.choice(School.objects.all())
    )

# Create results
for _ in range(150):
    Result.objects.create(
        date=fake.date_this_year(),
        student=random.choice(Student.objects.all()),
        exam=random.choice(Exam.objects.all()),
        score=random.uniform(0, 100),
        school=random.choice(School.objects.all())
    )

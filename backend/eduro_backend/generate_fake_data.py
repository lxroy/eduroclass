import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eduro_backend.settings")
django.setup()
from sms.models import School, Department, Teacher, Course, Student, Class, Attendance, Exam, Result
from faker import Faker
from django.core.wsgi import get_wsgi_application


fake = Faker()

# Import your models

# Sample data generation functions


def generate_school():
    return School.objects.create(
        name=fake.company(),
        address=fake.address(),
        school_type=fake.random_element(elements=('public', 'private')),
        accreditation_status=fake.word(),
        founding_date=fake.date(),
        principal_name=fake.name(),
        principal_email=fake.email(),
        principal_phone_number=fake.phone_number(),
        logo='path/to/your/logo/image.jpg',
        cover_picture='path/to/your/cover/image.jpg'
    )


def generate_department(school):
    return Department.objects.create(
        name=fake.word(),
        code=fake.word(),
        description=fake.sentence(),
        school=school
    )


def generate_teacher(department):
    return Teacher.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        department=department
    )


def generate_course(department, teachers):
    course = Course.objects.create(
        name=fake.word(),
        code=fake.word(),
        description=fake.sentence(),
        department=department
    )
    course.teachers.set(teachers)
    return course


def generate_student(courses):
    return Student.objects.create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        date_of_birth=fake.date_of_birth(),
        email=fake.email(),
        phone_number=fake.phone_number()
    )


def generate_class(courses, students):
    return Class.objects.create(
        name=fake.word(),
        description=fake.sentence()
    )


def generate_attendance(student, class_attended):
    return Attendance.objects.create(
        date=fake.date(),
        student=student,
        is_present=fake.boolean(),
        class_attended=class_attended
    )


def generate_exam(course, class_examined):
    return Exam.objects.create(
        date=fake.date(),
        start_time=fake.time(),
        end_time=fake.time(),
        venue=fake.word(),
        course=course,
        class_examined=class_examined
    )


def generate_result(student, exam):
    return Result.objects.create(
        date=fake.date(),
        student=student,
        exam=exam,
        score=fake.random_int(min=0, max=100)
    )


if __name__ == "__main__":
    # Create sample data
    school = generate_school()
    department = generate_department(school)
    teachers = [generate_teacher(department) for _ in range(5)]
    courses = [generate_course(department, teachers) for _ in range(5)]
    students = [generate_student(courses) for _ in range(20)]
    class_instance = generate_class(courses, students)

    # Populate attendance, exams, and results
    for student in students:
        generate_attendance(student, class_instance)
        course = fake.random_element(elements=courses)
        exam = generate_exam(course, class_instance)
        generate_result(student, exam)

    print("Sample data generation complete.")

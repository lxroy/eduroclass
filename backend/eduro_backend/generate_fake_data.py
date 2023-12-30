import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduro_backend.settings')
django.setup()
from sms.models import School, Department, Teacher, TeacherAssignment, Course, Student, Class, Attendance, Exam, Result
import random
from faker import Faker



fake = Faker()


def create_fake_schools(num_schools=10):
    for i in range(1, num_schools + 1):
        username = f'{fake.name()} school_{i}'
        name = fake.company()
        email = fake.email()
        School.objects.create(
            username=username,
            email=email,
            name=name,
            founding_date=fake.date_this_decade(),
            principal_name=fake.name(),
            principal_email=fake.email(),
            principal_phone_number=fake.phone_number(),
            telephone_number=fake.phone_number()
        )


def create_fake_departments(school, num_departments=3):
    for _ in range(num_departments):
        department = Department.objects.create(
            name=fake.word(),
            code=fake.word(),
            description=fake.text(),
            school=school,
            head_of_department=create_fake_teachers(
                school=school, num_teachers=1)[0],
        )
        create_fake_teacher_assignments(department)


def create_fake_teachers(school, num_teachers=5):
    teachers = []
    for i in range(num_teachers):
        teacher = Teacher.objects.create(
            username=f"{fake.user_name()}_{i}",
            email=fake.email(),
            password=fake.password(),
            school=school,
            dob=fake.date_of_birth(minimum_age=25, maximum_age=60),
            gender=random.choice(['male', 'female', 'others']),
            profile_picture=fake.image_url(),
            phone=fake.phone_number(),
            qualification=fake.word(),
        )
        teachers.append(teacher)
    return teachers


def create_fake_teacher_assignments(department, num_assignments=3):
    for _ in range(num_assignments):
        assignment = TeacherAssignment.objects.create(
            teacher=random.choice(
                Teacher.objects.filter(school=department.school)),
            department=department,
            course=create_fake_courses(
                department=department, num_courses=1)[0],
            school=department.school,
            active=True,
            date_of_joining=fake.date_between(
                start_date='-2y', end_date='today'),
            date_of_leave=fake.date_between(
                start_date='today', end_date='+1y') if random.choice([True, False]) else None,
        )
        if assignment.active:
            create_fake_students(assignment)


def create_fake_courses(department, num_courses=5):
    courses = []
    for _ in range(num_courses):
        course = Course.objects.create(
            name=fake.word(),
            code=fake.word(),
            description=fake.text(),
            department=department,
            syllabus=fake.text(),
        )
        courses.append(course)
    return courses


def create_fake_students(assignment, num_students=10):
    for i in range(num_students):
        student = Student.objects.create(
            username=f"{fake.user_name()}_{i}",
            email=fake.email(),
            password=fake.password(),
            school=assignment.school,
            dob=fake.date_of_birth(minimum_age=15, maximum_age=25),
            gender=random.choice(['male', 'female', 'others']),
            profile_picture=fake.image_url(),
            phone=fake.phone_number(),
            date_of_joining=fake.date_between(
                start_date='-1y', end_date='today'),
            date_of_leave=fake.date_between(
                start_date='today', end_date='+1y') if random.choice([True, False]) else None,
            active=True,
        )
        create_fake_attendances(student)


def create_fake_attendances(student, num_attendances=20):
    for _ in range(num_attendances):
        Attendance.objects.create(
            date=fake.date_between(start_date='-3m', end_date='today'),
            student=student,
            is_present=random.choice([True, False]),
            class_attended=random.choice(
                Class.objects.filter(students=student)),
            school=student.school,
            comments=fake.text() if random.choice([True, False]) else None,
        )


def create_fake_exams(num_exams=5):
    for _ in range(num_exams):
        courses = Course.objects.all()
        if courses.exists():
            exam = Exam.objects.create(
                date=fake.date_between(start_date='+1d', end_date='+30d'),
                start_time=fake.time(),
                end_time=fake.time(),
                venue=fake.word(),
                course=random.choice(courses),
                class_examined=random.choice(Class.objects.all()),
                school=random.choice(School.objects.all()),
                max_score=random.uniform(50, 100),
            )
            create_fake_results(exam)


def create_fake_results(exam, num_results=10):
    for _ in range(num_results):
        student = random.choice(Student.objects.all())
        score = random.uniform(0, exam.max_score)
        Result.objects.create(
            date=fake.date_between(start_date='-1y', end_date='today'),
            student=student,
            exam=exam,
            score=score,
            school=student.school,
            grade=get_grade(score),
        )


def create_fake_classes(num_classes=5):
    for _ in range(num_classes):
        departments = Department.objects.all()
        if departments.exists():
            random_department = random.choice(departments)
            Class.objects.create(
                name=fake.word(),
                description=fake.text(),
                courses=create_fake_courses(
                    department=random_department, num_courses=3),
                students=create_fake_students(assignment=random.choice(
                    TeacherAssignment.objects.filter(department=random_department)), num_students=20),
                start_date=fake.date_between(
                    start_date='-1y', end_date='today'),
                end_date=fake.date_between(start_date='today', end_date='+1y'),
            )



def get_grade(score):
    if score >= 90:
        return 'A'
    elif 80 <= score < 90:
        return 'B'
    elif 70 <= score < 80:
        return 'C'
    elif 60 <= score < 70:
        return 'D'
    else:
        return 'F'


def generate_fake_data():
    create_fake_schools()
    create_fake_exams()
    create_fake_classes()


if __name__ == '__main__':
    print("Starting Process......")
    generate_fake_data()
    print("Fake data added successfully.")

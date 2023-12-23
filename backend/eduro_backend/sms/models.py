from django.contrib.auth.models import User
from django.db import models


class SchoolManager(BaseUserManager):
    def create_school(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_school=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    name = models.CharField(max_length=255)
    address = models.TextField()
    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPES)
    accreditation_status = models.CharField(max_length=50)
    founding_date = models.DateField()
    principal_name = models.CharField(max_length=100)
    principal_email = models.EmailField()
    principal_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} - {self.course} at {self.school}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='teacher_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Student belongs to a single school
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='student_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Class(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    courses = models.ManyToManyField(Course)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.date} - Class: {self.class_attended}"


class Exam(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_examined = models.ForeignKey(Class, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course} - {self.date}"


class Result(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.exam} - Score: {self.score}"

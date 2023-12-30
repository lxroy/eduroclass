# models.py

from django.contrib.auth.models import BaseUserManager, AbstractUser, Group, Permission
from django.db import models


class SchoolManager(BaseUserManager):
    def create_school(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_school=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class School(AbstractUser):
    objects = SchoolManager()

    is_school = models.BooleanField(default=True)

    SCHOOL_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    name = models.CharField(max_length=255)
    address = models.TextField()
    school_type = models.CharField(max_length=10, choices=SCHOOL_TYPES)
    founding_date = models.DateField()
    principal_name = models.CharField(max_length=100)
    principal_email = models.EmailField()
    principal_phone_number = models.CharField(max_length=15)
    telephone_number = models.CharField(max_length=15, null=True, blank=True)

    # Adding related_name attributes to resolve clash
    groups = models.ManyToManyField(Group, related_name='school_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='school_user_permissions'
    )

    profile_picture = models.ImageField(
        upload_to='school_profiles/', null=True, blank=True)

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
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
        return f'{self.teacher} - {self.course}'


class TeacherManager(BaseUserManager):
    def create_teacher(self, username, email, password=None, school=None, **extra_fields):
        if school is None:
            raise ValueError("A teacher must be associated with a school.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_teacher=True, school=school, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Teacher(AbstractUser):
    objects = TeacherManager()

    is_teacher = models.BooleanField(default=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    # Adding related_name attributes to resolve clash
    groups = models.ManyToManyField(Group, related_name='teacher_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='teacher_user_permissions'
    )

    profile_picture = models.ImageField(
        upload_to='teacher_profiles/', null=True, blank=True)

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StudentManager(BaseUserManager):
    def create_student(self, username, email, password=None, school=None, **extra_fields):
        if school is None:
            raise ValueError("A student must be associated with a school.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_student=True, school=school, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Student(AbstractUser):
    objects = StudentManager()

    is_student = models.BooleanField(default=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    # Adding related_name attributes to resolve clash
    groups = models.ManyToManyField(Group, related_name='student_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='student_user_permissions'
    )

    profile_picture = models.ImageField(
        upload_to='student_profiles/', null=True, blank=True)

    def __str__(self):
        return self.username


class Class(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    courses = models.ManyToManyField(Course)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField()
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student} - {self.date}'


class Exam(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_examined = models.ForeignKey(Class, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course} - {self.date}'


class Result(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student} - {self.exam}'

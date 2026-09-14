from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=100, default="BCA")
    semester = models.CharField(max_length=50, default="5th Semester")

    def __str__(self):
        return self.user.username


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    attended_classes = models.PositiveIntegerField(default=0)
    total_classes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"


class InternalMark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"


class Timetable(models.Model):
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=30)
    subject = models.CharField(max_length=100)
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.day} - {self.time} - {self.subject}"


class ExamSchedule(models.Model):
    exam_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()
    exam_time = models.CharField(max_length=30)
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.subject} - {self.exam_date}"


class Assignment(models.Model):
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.subject} - {self.title}"


class StudyMaterial(models.Model):
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject} - {self.title}"
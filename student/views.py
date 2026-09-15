from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from groq import Groq

from .models import (
    StudentProfile,
    Attendance,
    InternalMark,
    Timetable,
    ExamSchedule,
    Assignment,
    StudyMaterial,
)


def home(request):
    return render(request, "student/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect("/admin/")

            return redirect("dashboard")

        return render(
            request,
            "student/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "student/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    attendance = Attendance.objects.filter(student=request.user)
    marks = InternalMark.objects.filter(student=request.user)
    timetable = Timetable.objects.all()
    exams = ExamSchedule.objects.all()
    assignments = Assignment.objects.all()
    study_materials = StudyMaterial.objects.all()

    return render(
        request,
        "student/dashboard.html",
        {
            "attendance": attendance,
            "marks": marks,
            "timetable": timetable,
            "exams": exams,
            "assignments": assignments,
            "study_materials": study_materials,
        }
    )


@login_required
def ai_assistant(request):
    answer = None

    attendance = Attendance.objects.filter(student=request.user)
    marks = InternalMark.objects.filter(student=request.user)
    timetable = Timetable.objects.all()
    exams = ExamSchedule.objects.all()
    assignments = Assignment.objects.all()
    study_materials = StudyMaterial.objects.all()

    attendance_data = ""
    for item in attendance:
        attendance_data += (
            f"{item.subject}: "
            f"{item.attended_classes} attended out of "
            f"{item.total_classes} classes\n"
        )

    marks_data = ""
    for item in marks:
        marks_data += f"{item.subject}: {item.marks} marks\n"

    timetable_data = ""
    for item in timetable:
        timetable_data += (
            f"{item.day} - {item.time} - "
            f"{item.subject} - Room {item.room}\n"
        )

    exam_data = ""
    for item in exams:
        exam_data += (
            f"{item.exam_name} - {item.subject} - "
            f"{item.exam_date} - {item.exam_time} - "
            f"Room {item.room}\n"
        )

    assignment_data = ""
    for item in assignments:
        assignment_data += (
            f"{item.subject} - "
            f"{item.title} - Due: {item.due_date}\n"
        )

    study_material_data = ""
    for item in study_materials:
        study_material_data += (
            f"{item.subject} - "
            f"{item.title} - {item.description}\n"
        )

    if request.method == "POST":
        question = request.POST.get("question")

        client = Groq(api_key=settings.GROQ_API_KEY)

        system_prompt = f"""
You are an AI College Assistant.

The student you are talking to is:
{request.user.username}

Use the following database information when answering
questions about the student's college information.

STUDENT ATTENDANCE:
{attendance_data}

STUDENT INTERNAL MARKS:
{marks_data}

COLLEGE TIMETABLE:
{timetable_data}

EXAM SCHEDULE:
{exam_data}

ASSIGNMENTS:
{assignment_data}

STUDY MATERIALS:
{study_material_data}

Important rules:

1. If the student asks about their attendance, use the attendance data above.
2. If the student asks about their marks, use the marks data above.
3. If the student asks about timetable, use the timetable data above.
4. If the student asks about exams, use the exam schedule above.
5. If the student asks about assignments, use the assignment data above.
6. If the student asks about study materials, use the study material data above.
7. Do not invent student-specific information.
8. If information is not available in the database, clearly say that it is not available.
9. Answer in a clear, simple and friendly way.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        answer = response.choices[0].message.content

    return render(
        request,
        "student/ai.html",
        {"answer": answer}
    )


def create_student(request):
    student, created = User.objects.get_or_create(
        username="Student01"
    )

    student.set_password("Student@12345")
    student.is_active = True
    student.is_staff = False
    student.is_superuser = False
    student.save()

    return redirect("login")
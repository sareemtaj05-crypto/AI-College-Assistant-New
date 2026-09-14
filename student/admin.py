from django.contrib import admin
from .models import (
    StudentProfile,
    Attendance,
    InternalMark,
    Timetable,
    ExamSchedule,
    Assignment,
    StudyMaterial,
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "semester")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "attended_classes",
        "total_classes",
    )
    list_filter = ("subject", "student")


@admin.register(InternalMark)
class InternalMarkAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "marks",
    )
    list_filter = ("subject", "student")


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        "day",
        "time",
        "subject",
        "room",
    )
    list_filter = ("day",)


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "exam_name",
        "subject",
        "exam_date",
        "exam_time",
        "room",
    )
    list_filter = ("exam_name", "subject")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "title",
        "due_date",
    )
    list_filter = ("subject",)


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "title",
    )
    list_filter = ("subject",)
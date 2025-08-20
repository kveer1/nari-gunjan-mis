

# Register your models here.
from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance, CMAttendance

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'present']
    list_filter = ['date', 'present']

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'date', 'present']
    list_filter = ['date', 'present']

@admin.register(CMAttendance)
class CMAttendanceAdmin(admin.ModelAdmin):
    list_display = ['cm', 'date', 'present']
    list_filter = ['date', 'present']
    

# Register your models here.
from django.contrib import admin
from .models import LearningCenter, Teacher, CommunityMobilizer, Student

@admin.register(LearningCenter)
class LearningCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'village', 'block']
    search_fields = ['name', 'village']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'center', 'date_of_joining']
    list_filter = ['center', 'date_of_joining']

@admin.register(CommunityMobilizer)
class CommunityMobilizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_of_joining']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'center', 'gender', 'current_level', 'enrolled_in_govt_school']
    list_filter = ['center', 'gender', 'enrolled_in_govt_school']
    search_fields = ['name', 'mother_name', 'father_name']
    
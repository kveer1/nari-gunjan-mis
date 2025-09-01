
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_dashboard, name='attendance_dashboard'),
    path('student/', views.mark_student_attendance, name='mark_student_attendance'),
    path('teacher/', views.mark_teacher_attendance, name='mark_teacher_attendance'),
    path('cm/', views.mark_cm_attendance, name='mark_cm_attendance'),
    path('bulk/student/', views.bulk_student_attendance, name='bulk_student_attendance'),
    path('bulk/student/center/<int:center_id>/', views.bulk_student_attendance, name='bulk_student_attendance_center'),
    path('success/', views.attendance_success, name='attendance_success'),
]
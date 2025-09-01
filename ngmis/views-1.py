from django.http import HttpResponse

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student, LearningCenter
from attendance.models import StudentAttendance
from django.utils import timezone
from django.db.models import Count, Q

@login_required
@login_required
def dashboard(request):
    # Get user role from profile
    user_role = None
    if hasattr(request.user, 'userprofile'):
        user_role = request.user.userprofile.role
    else:
        # Default to admin for users without profile (like superuser)
        user_role = 'admin'
    
    # Route to appropriate dashboard based on role
    if user_role == 'teacher':
        return teacher_dashboard(request)
    elif user_role == 'cm':
        return cm_dashboard(request)
    elif user_role == 'coordinator':
        return coordinator_dashboard(request)
    elif user_role == 'manager':
        return manager_dashboard(request)
    else:  # admin and others
        return admin_dashboard(request)

def admin_dashboard(request):
    """Dashboard for admin users"""
    # Get basic statistics
    total_students = Student.objects.count()
    active_centers = LearningCenter.objects.count()
    
    # Get gender distribution
    gender_distribution = Student.objects.aggregate(
        boys=Count('id', filter=Q(gender='MALE')),
        girls=Count('id', filter=Q(gender='FEMALE'))
    )
    
    # Get today's attendance
    today = timezone.now().date()
    today_attendance = StudentAttendance.objects.filter(date=today, present=True).count()
    total_today_attendance = StudentAttendance.objects.filter(date=today).count()
    
    context = {
        'total_students': total_students,
        'active_centers': active_centers,
        'boys_count': gender_distribution.get('boys', 0) or 0,
        'girls_count': gender_distribution.get('girls', 0) or 0,
        'today_attendance': today_attendance,
        'total_today_attendance': total_today_attendance,
        'attendance_date': today,
    }
    
    return render(request, 'dashboard.html', context)

# Add other dashboard functions (you can implement these later)
def teacher_dashboard(request):
    return admin_dashboard(request)  # For now, use same as admin

def cm_dashboard(request):
    return admin_dashboard(request)  # For now, use same as admin

def coordinator_dashboard(request):
    return admin_dashboard(request)  # For now, use same as admin

def manager_dashboard(request):
    return admin_dashboard(request)  # For now, use same as admin

def teacher_dashboard(request):
    # Get teacher's assigned centers
    centers = request.user.userprofile.assigned_centers.all()
    students = Student.objects.filter(center__in=centers)
    
    context = {
        'centers': centers,
        'student_count': students.count(),
        'recent_attendance': StudentAttendance.objects.filter(
            student__in=students
        ).order_by('-date')[:5]
    }
    return render(request, 'dashboard_teacher.html', context)

def cm_dashboard(request):
    # Similar implementation for CM
    centers = request.user.userprofile.assigned_centers.all()
    context = {
        'centers': centers,
        'center_count': centers.count()
    }
    return render(request, 'dashboard_cm.html', context)

# Add similar functions for other roles

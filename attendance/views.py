from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import StudentAttendance, TeacherAttendance, CMAttendance
from .forms import StudentAttendanceForm, TeacherAttendanceForm, CMAttendanceForm, BulkStudentAttendanceForm
from students.models import Student, LearningCenter

from django.contrib.auth.decorators import login_required, user_passes_test

def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'teacher'

def is_cm(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'cm'

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'admin'

@login_required
@user_passes_test(lambda user: is_teacher(user) or is_admin(user))
def mark_student_attendance(request):
    if request.method == 'POST':
        form = StudentAttendanceForm(request.POST)
        if form.is_valid():
            try:
                attendance = form.save(commit=False)
                attendance.marked_by = request.user
                attendance.save()
                messages.success(request, f"Attendance marked for {attendance.student.name}")
                return redirect('mark_student_attendance')
            except Exception as e:
                messages.error(request, f"Error saving attendance: {str(e)}")
    else:
        form = StudentAttendanceForm()
    
    # Get recent attendance records
    recent_attendance = StudentAttendance.objects.all().order_by('-date')[:10]
    
    return render(request, 'attendance/mark_student.html', {
        'form': form,
        'recent_attendance': recent_attendance
    })

@login_required
@user_passes_test(lambda user: is_admin(user))
def mark_teacher_attendance(request):
    if request.method == 'POST':
        form = TeacherAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, f"Attendance marked for {attendance.teacher.name}")
            return redirect('mark_teacher_attendance')
    else:
        form = TeacherAttendanceForm()
    
    return render(request, 'attendance/mark_teacher.html', {'form': form})

@login_required
def mark_cm_attendance(request):
    if request.method == 'POST':
        form = CMAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, f"Attendance marked for {attendance.cm.name}")
            return redirect('mark_cm_attendance')
    else:
        form = CMAttendanceForm()
    
    return render(request, 'attendance/mark_cm.html', {'form': form})

@login_required
def bulk_student_attendance(request, center_id=None):
    center = None
    if center_id:
        center = get_object_or_404(LearningCenter, id=center_id)
    
    if request.method == 'POST':
        form = BulkStudentAttendanceForm(request.POST, center=center)
        if form.is_valid():
            date = form.cleaned_data['date']
            students = form.cleaned_data['students']
            
            count = 0
            for student in students:
                # Create or update attendance record
                attendance, created = StudentAttendance.objects.get_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'present': True,
                        'marked_by': request.user
                    }
                )
                if not created:
                    attendance.present = True
                    attendance.marked_by = request.user
                    attendance.save()
                count += 1
            
            messages.success(request, f"Attendance marked for {count} students")
            return redirect('bulk_student_attendance')
    else:
        form = BulkStudentAttendanceForm(center=center)
    
    centers = LearningCenter.objects.all()
    return render(request, 'attendance/bulk_student.html', {
        'form': form,
        'centers': centers,
        'selected_center': center
    })

@login_required
def attendance_dashboard(request):
    today = timezone.now().date()
    
    # Basic statistics
    student_attendance_today = StudentAttendance.objects.filter(date=today)
    teacher_attendance_today = TeacherAttendance.objects.filter(date=today)
    cm_attendance_today = CMAttendance.objects.filter(date=today)
    
    # Monthly statistics
    from datetime import timedelta
    month_start = today.replace(day=1)
    student_monthly = StudentAttendance.objects.filter(date__gte=month_start)
    
    context = {
        'student_attendance_count': student_attendance_today.count(),
        'teacher_attendance_count': teacher_attendance_today.count(),
        'cm_attendance_count': cm_attendance_today.count(),
        'monthly_count': student_monthly.count(),
        'today': today,
    }
    
    return render(request, 'attendance/dashboard.html', context)
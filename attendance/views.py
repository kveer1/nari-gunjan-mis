from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from .models import StudentAttendance, TeacherAttendance, CMAttendance
from .forms import StudentAttendanceForm, TeacherAttendanceForm, CMAttendanceForm, BulkStudentAttendanceForm
from students.models import Student, LearningCenter

@login_required
def attendance_dashboard(request):
    """Main attendance dashboard"""
    today = timezone.now().date()
    
    # Basic statistics
    student_attendance_today = StudentAttendance.objects.filter(date=today)
    teacher_attendance_today = TeacherAttendance.objects.filter(date=today)
    cm_attendance_today = CMAttendance.objects.filter(date=today)
    
    context = {
        'student_attendance_count': student_attendance_today.count(),
        'teacher_attendance_count': teacher_attendance_today.count(),
        'cm_attendance_count': cm_attendance_today.count(),
        'today': today,
    }
    
    return render(request, 'attendance/dashboard.html', context)

@login_required
def mark_student_attendance(request):
    """Mark individual student attendance"""
    if request.method == 'POST':
        form = StudentAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            messages.success(request, f"Attendance marked for {attendance.student.name}")
            return redirect('mark_student_attendance')
    else:
        form = StudentAttendanceForm()
    
    recent_attendance = StudentAttendance.objects.all().order_by('-date')[:10]
    
    return render(request, 'attendance/mark_student.html', {
        'form': form,
        'recent_attendance': recent_attendance
    })

@login_required
def mark_teacher_attendance(request):
    """Mark teacher attendance"""
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
    """Mark community mobilizer attendance"""
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
    """Bulk student attendance marking"""
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
                        'marked_by': request.user,
                        'remarks': 'Bulk attendance marking'
                    }
                )
                if not created:
                    attendance.present = True
                    attendance.marked_by = request.user
                    attendance.remarks = 'Updated via bulk marking'
                    attendance.save()
                count += 1
            
            messages.success(request, f"✅ Attendance marked for {count} students on {date}")
            return redirect('bulk_student_attendance')
    else:
        # Pre-select all students by default
        initial = {'select_all': True}
        if center:
            initial['students'] = Student.objects.filter(center=center)
        form = BulkStudentAttendanceForm(center=center, initial=initial)
    
    centers = LearningCenter.objects.all()
    return render(request, 'attendance/bulk_student.html', {
        'form': form,
        'centers': centers,
        'selected_center': center
    })

@login_required
def attendance_success(request):
    """Display success message after marking attendance"""
    return render(request, 'attendance/success.html')
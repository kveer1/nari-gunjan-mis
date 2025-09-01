
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q, Avg
from django.http import JsonResponse
from datetime import datetime, timedelta
from students.models import Student, LearningCenter
from attendance.models import StudentAttendance

@login_required
def attendance_reports(request):
    """Main reports dashboard"""
    return render(request, 'reports/attendance_reports.html')

@login_required
def attendance_calendar_view(request):
    """Calendar view of attendance"""
    # Get date range (default: current month)
    today = timezone.now().date()
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    
    # Get attendance data for the month
    start_date = datetime(int(year), int(month), 1).date()
    if int(month) == 12:
        end_date = datetime(int(year) + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(int(year), int(month) + 1, 1).date() - timedelta(days=1)
    
    # Get attendance data
    attendance_data = StudentAttendance.objects.filter(
        date__range=[start_date, end_date]
    ).values('date').annotate(
        total=Count('id'),
        present=Count('id', filter=Q(present=True)),
        absent=Count('id', filter=Q(present=False))
    ).order_by('date')
    
    context = {
        'year': year,
        'month': month,
        'start_date': start_date,
        'end_date': end_date,
        'attendance_data': attendance_data,
        'centers': LearningCenter.objects.all(),
    }
    return render(request, 'reports/attendance_calendar.html', context)

@login_required
def attendance_drilldown(request, period, year, month=None, week=None):
    """Drill-down attendance reports"""
    today = timezone.now().date()
    
    if period == 'year':
        # Yearly view -> show months
        start_date = datetime(int(year), 1, 1).date()
        end_date = datetime(int(year), 12, 31).date()
        data = get_monthly_attendance(int(year))
        template = 'reports/yearly_report.html'
        
    elif period == 'month':
        # Monthly view -> show weeks
        start_date = datetime(int(year), int(month), 1).date()
        if int(month) == 12:
            end_date = datetime(int(year) + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(int(year), int(month) + 1, 1).date() - timedelta(days=1)
        data = get_weekly_attendance(int(year), int(month))
        template = 'reports/monthly_report.html'
        
    elif period == 'week':
        # Weekly view -> show days
        start_date = get_week_start_date(int(year), int(week))
        end_date = start_date + timedelta(days=6)
        data = get_daily_attendance(start_date, end_date)
        template = 'reports/weekly_report.html'
    
    else:
        # Custom period
        start_date = request.GET.get('start_date', today - timedelta(days=30))
        end_date = request.GET.get('end_date', today)
        data = get_daily_attendance(start_date, end_date)
        template = 'reports/custom_report.html'
    
    context = {
        'period': period,
        'year': year,
        'month': month,
        'week': week,
        'start_date': start_date,
        'end_date': end_date,
        'attendance_data': data,
        'centers': LearningCenter.objects.all(),
    }
    return render(request, template, context)

@login_required
def exception_reports(request):
    """Exception reports for management"""
    # Students absent for more than a week
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Get students absent for more than a week
    chronically_absent = Student.objects.filter(
        studentattendance__date__gte=week_ago,
        studentattendance__present=False
    ).annotate(
        absent_days=Count('studentattendance', filter=Q(studentattendance__present=False))
    ).filter(absent_days__gte=5).distinct()
    
    # Center-wise attendance issues
    center_issues = []
    for center in LearningCenter.objects.all():
        attendance_rate = StudentAttendance.get_attendance_stats(
            week_ago, today, center
        )['attendance_rate']
        if attendance_rate < 80:  # Less than 80% attendance
            center_issues.append({
                'center': center,
                'attendance_rate': attendance_rate,
                'issues': f"Low attendance rate: {attendance_rate:.1f}%"
            })
    
    context = {
        'chronically_absent': chronically_absent,
        'center_issues': center_issues,
        'start_date': week_ago,
        'end_date': today,
    }
    return render(request, 'reports/exception_reports.html', context)

# Utility functions
def get_monthly_attendance(year):
    """Get monthly attendance data for a year"""
    monthly_data = []
    for month in range(1, 13):
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
        stats = StudentAttendance.get_attendance_stats(start_date, end_date)
        monthly_data.append({
            'month': start_date.strftime('%B'),
            'start_date': start_date,
            'end_date': end_date,
            **stats
        })
    return monthly_data

def get_weekly_attendance(year, month):
    """Get weekly attendance data for a month"""
    weekly_data = []
    start_date = datetime(year, month, 1).date()
    current_date = start_date
    
    while current_date.month == month:
        week_end = current_date + timedelta(days=6)
        if week_end.month != month:
            week_end = datetime(year, month, 1).date().replace(day=1) + timedelta(days=32)
            week_end = week_end.replace(day=1) - timedelta(days=1)
        
        stats = StudentAttendance.get_attendance_stats(current_date, week_end)
        weekly_data.append({
            'week': f"Week {len(weekly_data) + 1}",
            'start_date': current_date,
            'end_date': week_end,
            **stats
        })
        
        current_date = week_end + timedelta(days=1)
    
    return weekly_data

def get_daily_attendance(start_date, end_date):
    """Get daily attendance data for a period"""
    daily_data = []
    current_date = start_date
    
    while current_date <= end_date:
        stats = StudentAttendance.get_attendance_stats(current_date, current_date)
        daily_data.append({
            'date': current_date,
            **stats
        })
        current_date += timedelta(days=1)
    
    return daily_data

def get_week_start_date(year, week):
    """Get start date for a given week number"""
    jan_first = datetime(year, 1, 1).date()
    start_date = jan_first + timedelta(weeks=week-1)
    # Adjust to Monday
    while start_date.weekday() != 0:  # 0 is Monday
        start_date -= timedelta(days=1)
    return start_date



#below is old code to be deleted

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from students.models import Student, LearningCenter
from attendance.models import StudentAttendance

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    # Teacher dashboard
    if hasattr(user, 'teacher'):
        teacher = user.teacher
        center = teacher.center
        students = Student.objects.filter(center=center)
        context.update({
            'center': center,
            'students': students,
            'total_students': students.count(),
            'male_students': students.filter(gender='MALE').count(),
            'female_students': students.filter(gender='FEMALE').count(),
        })
    
    # Admin dashboard
    elif user.is_superuser:
        centers = LearningCenter.objects.all()
        students = Student.objects.all()
        context.update({
            'centers': centers,
            'total_students': students.count(),
            'total_centers': centers.count(),
        })
    
    return render(request, 'dashboard.html', context)


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_centers = LearningCenter.objects.count()
    
    # Count students by gender
    male_students = Student.objects.filter(gender='MALE').count()
    female_students = Student.objects.filter(gender='FEMALE').count()
    
    context = {
        'total_students': total_students,
        'total_centers': total_centers,
        'male_students': male_students,
        'female_students': female_students,
    }
    
    return render(request, 'dashboard.html', context)




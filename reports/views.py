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
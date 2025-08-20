
# Create your models here.

from django.db import models
from students.models import LearningCenter, Student, Teacher, CommunityMobilizer

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('student', 'date')
        app_label = 'attendance'

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('teacher', 'date')
        app_label = 'attendance'

class CMAttendance(models.Model):
    cm = models.ForeignKey(CommunityMobilizer, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    centers_visited = models.ManyToManyField(LearningCenter, blank=True)
    remarks = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('cm', 'date')
        app_label = 'attendance'
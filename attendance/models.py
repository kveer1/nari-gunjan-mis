
from django.db import models
from django.contrib.auth.models import User
from students.models import Student, Teacher, CommunityMobilizer

class AttendanceBaseModel(models.Model):
    date = models.DateField()
    present = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class StudentAttendance(AttendanceBaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student__name']
    
    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.student.name} - {self.date} - {status}"
    
    @classmethod
    def get_attendance_stats(cls, start_date, end_date, center=None):
        """Get comprehensive attendance statistics"""
        queryset = cls.objects.filter(date__range=[start_date, end_date])
        if center:
            queryset = queryset.filter(student__center=center)
        
        total_records = queryset.count()
        present_count = queryset.filter(present=True).count()
        absent_count = total_records - present_count
        
        return {
            'total': total_records,
            'present': present_count,
            'absent': absent_count,
            'attendance_rate': (present_count / total_records * 100) if total_records > 0 else 0
        }

class TeacherAttendance(AttendanceBaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('teacher', 'date')
        ordering = ['-date', 'teacher__name']

class CMAttendance(AttendanceBaseModel):
    cm = models.ForeignKey(CommunityMobilizer, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('cm', 'date')
        ordering = ['-date', 'cm__name']
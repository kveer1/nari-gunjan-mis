
from django import forms
from .models import StudentAttendance, TeacherAttendance, CMAttendance
from students.models import Student
from django.utils import timezone

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = ['student', 'date', 'present', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'value': timezone.now().date()
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control'
            }),
        }

class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = TeacherAttendance
        fields = ['teacher', 'date', 'present', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'value': timezone.now().date()
            }),
        }

class CMAttendanceForm(forms.ModelForm):
    class Meta:
        model = CMAttendance
        fields = ['cm', 'date', 'present', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'value': timezone.now().date()
            }),
        }

class BulkStudentAttendanceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'value': timezone.now().date()
        })
    )
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        center = kwargs.pop('center', None)
        super().__init__(*args, **kwargs)
        if center:
            self.fields['students'].queryset = Student.objects.filter(center=center)
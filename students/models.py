from django.db import models
from django.contrib.auth.models import User

class LearningCenter(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    village = models.CharField(max_length=100)
    gram_panchayat = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'students'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    contact_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'students'

class CommunityMobilizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    
    def __str__(self):
        return self.name

    class Meta:
        app_label = 'students'

class Student(models.Model):
    GENDER_CHOICES = [('MALE', 'Male'), ('FEMALE', 'Female')]
    
    name = models.CharField(max_length=100)
    date_of_enrollment = models.DateField()
    child_id = models.CharField(max_length=20, blank=True)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    current_level = models.IntegerField()
    current_class = models.IntegerField()
    enrolled_in_govt_school = models.BooleanField(default=False)
    govt_school_class = models.IntegerField(blank=True, null=True)
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    def age(self):
        import datetime
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

    class Meta:
        app_label = 'students'
        
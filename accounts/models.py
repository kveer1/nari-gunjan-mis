# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from students.models import LearningCenter

class UserProfile(models.Model):
    USER_ROLES = (
        ('teacher', 'Teacher'),
        ('cm', 'Community Mobilizer'),
        ('coordinator', 'Project Coordinator'),
        ('manager', 'Project Manager'),
        ('admin', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    phone = models.CharField(max_length=15, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    assigned_centers = models.ManyToManyField(LearningCenter, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
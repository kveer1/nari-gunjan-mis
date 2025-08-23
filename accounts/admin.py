
# Register your models here.
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'date_of_joining']
    list_filter = ['role']
    filter_horizontal = ['assigned_centers']
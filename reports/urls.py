from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_reports, name='attendance_reports'),
    path('calendar/', views.attendance_calendar_view, name='attendance_calendar'),
    
    # Separate URL patterns for each parameter combination
    path('drilldown/year/<int:year>/', views.attendance_drilldown, name='attendance_drilldown_year'),
    path('drilldown/month/<int:year>/<int:month>/', views.attendance_drilldown, name='attendance_drilldown_month'),
    path('drilldown/week/<int:year>/<int:month>/<int:week>/', views.attendance_drilldown, name='attendance_drilldown_week'),
    path('drilldown/custom/', views.attendance_drilldown, name='attendance_drilldown_custom'),
    
    path('exceptions/', views.exception_reports, name='exception_reports'),
]
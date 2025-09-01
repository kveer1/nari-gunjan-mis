from django.urls import path
from . import views

from . import views

urlpatterns = [
    path('', views.attendance_reports, name='attendance_reports'),
    path('calendar/', views.attendance_calendar_view, name='attendance_calendar'),
    path('drilldown/<str:period>/<int:year>/', views.attendance_drilldown, name='attendance_drilldown'),
    path('drilldown/<str:period>/<int:year>/<int:month>/', views.attendance_drilldown, name='attendance_drilldown_month'),
    path('drilldown/<str:period>/<int:year>/<int:month>/<int:week>/', views.attendance_drilldown, name='attendance_drilldown_week'),
    path('exceptions/', views.exception_reports, name='exception_reports'),
]
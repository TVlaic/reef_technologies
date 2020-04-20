from django.urls import path
from app_hubstaff.views import index, login, mock_login, logout, timesheet_report


urlpatterns = [
    path('', index),
    path('login', login),
    path('mock_login', mock_login),
    path('logout', logout),
    path('timesheet_report',timesheet_report)
]

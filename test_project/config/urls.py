from django.urls import path, include
import app_hubstaff 

urlpatterns = [
    path('', include(("app_hubstaff.urls"))),
]

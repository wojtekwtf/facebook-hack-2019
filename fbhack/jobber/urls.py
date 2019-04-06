from django.urls import path

from .views import home, check_job

urlpatterns = [
    path('', home, name='jobber-home'),
    path('check', check_job, name='check'),
]
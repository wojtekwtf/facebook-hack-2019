from django.urls import path

from .views import home, check_job, find_job, recommend_job, about, team

urlpatterns = [
    path('', home, name='jobber-home'),
    path('check', check_job, name='check'),
    path('find', find_job, name='find'),
    path('about', about, name='about'),
    path('team', team, name='team'),
]
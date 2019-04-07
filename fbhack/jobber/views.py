from django.shortcuts import render, redirect
from .models import Recomendation
from jobber.models import Job
from deep_person.auto import is_dying
from deep_person.stable import sentence_mean
from deep_person.l1 import l1_score, ref
from difflib import get_close_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests
from bs4 import BeautifulSoup
from yt_recommender import youtube_search

def home(request):
    context = {}
    if request.method == 'POST':
        job_name = request.POST['job']
        jobs = [job.job for job in Job.objects.all()]
        x, _ = process.extract(job_name, jobs, scorer=fuzz.ratio)[0]
        danger = 'unsafe' if is_dying(x) else 'safe'
        #job_obj = Job.objects.filter(job__icontains=job_name).first()
        #danger = 'safe' if job_obj.probability < 0.5 else 'unsafe'
        context = {
            'job': job_name,
            'danger': danger
        }
        return check_job(request, context)

    return render(request, 'jobber/homepage.html', context)


def check_job(request, context):
    return render(request, 'jobber/jobfinder.html', context)


def get_job_from_tags(text_to_analize):
    v1 = sentence_mean(text_to_analize)
    return l1_score(v1, ref)

def find_job(request):
    if request.method == 'POST':
        text_to_analize = ''
        for text in range(3):
            text_to_analize += " "+str(request.POST[f'job{text}'])
        future_job = get_job_from_tags(text_to_analize)
        return recommend_job(request, future_job)
    return render(request, 'jobber/check.html')


def get_recoms(job):
    return Recomendation.objects.filter(
        job__icontains=job
    ).order_by('?')

def recommend_job(request, future_job):
    # LOAD DATA FROM DB
    jobs = get_recoms(future_job)
    context = {
        'job': future_job,
        'data': jobs,
        
    }
    return render(request, 'jobber/recommend.html', context)

# Create your views here.

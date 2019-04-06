from django.shortcuts import render, redirect
from jobber.models import Job
#from deep_person.auto import is_dying
from deep_person.stable import sentence_mean
from deep_person.l1 import l1_score, ref


def home(request):
    context = {}
    if request.method == 'POST':
        job_name = request.POST['job']
        #danger = 'safe' if is_dying(job_name) < 0.5 else 'unsafe'
        job_obj = Job.objects.filter(job__icontains=job_name).first()
        danger = 'safe' if job_obj.probability < 0.5 else 'unsafe'
        context = {
            'job': job_name,
            'danger': danger
        }
        return check_job(request, context)
    
    return render(request,'jobber/homepage.html',context)


def check_job(request, context):
    return render(request,'jobber/jobfinder.html',context)

def get_job_from_tags(text_to_analize):
    v1 = sentence_mean(text_to_analize)
    return l1_score(v1, ref)


def find_job(request):
    if request.method == 'POST':
        text_to_analize = ''
        for text in range(3):
            text_to_analize+= " "+str(request.POST[f'job{text}'])
        future_job = get_job_from_tags(text_to_analize)
        return recommend_job(request, future_job)
    return render(request,'jobber/check.html')

def recommend_job(request, future_job):
    context = {
            'job': future_job,
            'links': 'link'
        }
    return render(request,'jobber/recommend.html', context)

# Create your views here.

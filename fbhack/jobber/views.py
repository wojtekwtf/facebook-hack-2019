from django.shortcuts import render, redirect
from jobber.models import Job



def home(request):
    context = {}
    if request.method == 'POST':
        job_name = request.POST['job']
        job_obj = Job.objects.filter(job__icontains=job_name).first()
        danger = 'safe' if job_obj.probability < 0.5 else 'unsafe'
        context = {
            'job': job_obj.job,
            'danger': danger
        }
        return check_job(request, context)
    
    return render(request,'jobber/homepage.html',context)


def check_job(request, context):
    return render(request,'jobber/jobfinder.html',context)

def find_job(request):
    return render(request,'jobber/check.html')


# Create your views here.

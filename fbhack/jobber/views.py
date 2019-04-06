from django.shortcuts import render, redirect
from jobber.models import Job
#from deep_person.auto import is_dying



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
    # CODE
    return 'Developer'


def find_job(request):
    if request.method == 'POST':
        text_to_analize = ''
        for text in range(3):
            text_to_analize+= " "+str(request.POST[f'job{text}'])
        future_job = get_job_from_tags(text_to_analize)
        #return redirect('recommendation', job=future_job)
        return recommend_job(request, future_job)
    return render(request,'jobber/check.html')

def recommend_job(request, future_job):
    print(request)
    print(future_job)
    return render(request,'jobber/recommend.html')

# Create your views here.

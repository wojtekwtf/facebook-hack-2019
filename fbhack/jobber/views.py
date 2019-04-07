from django.shortcuts import render, redirect
from jobber.models import Job
from deep_person.auto import is_dying
from deep_person.stable import sentence_mean
from deep_person.l1 import l1_score, ref
from difflib import get_close_matches
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests
from bs4 import BeautifulSoup


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
    # v1 = sentence_mean(text_to_analize)
    # return l1_score(v1, ref)
    return "Chef"

def find_job(request):
    if request.method == 'POST':
        text_to_analize = ''
        for text in range(3):
            text_to_analize += " "+str(request.POST[f'job{text}'])
        future_job = get_job_from_tags(text_to_analize)
        return recommend_job(request, future_job)
    return render(request, 'jobber/check.html')


def get_jobs_from_quora(job):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.11 (KHTML, like Gecko) '
        'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    job_name = job.replace(' ', '+')
    link = f'https://www.quora.com/search?q=how+to+become+{job_name}'

    soup = BeautifulSoup(
        requests.get(
            link,
            timeout=4,
            headers=headers
        ).text,
        'html.parser'
    )

    x = soup.find_all('div', class_='pagedlist_item')
    links = []
    for m in x[:6]:
        links.append(f"https://www.quora.com{m.find('a', class_='question_link').get('href')}")
    data = []
    for link in links[:4]:
        soup = BeautifulSoup(
            requests.get(
                link,
                timeout=4,
                headers=headers
            ).text,
            'html.parser'
        )
        title = soup.find('div', class_='question_text_edit').find(
            'span', class_='ui_qtext_rendered_qtext').text
        content = soup.find('div', class_='pagedlist_item').find('div', class_='Answer').find_all(
            'p', class_='ui_qtext_para u-ltr u-text-align--start')
        text_togheter = ''
        for t in content:
            text_togheter += f' {t.text}'
        data.append({
            'link': link,
            'title': title,
            'content': text_togheter
        })
    return data


def recommend_job(request, future_job):
    data = get_jobs_from_quora(future_job)
    context = {
        'job': future_job,
        'recommendation': data
    }
    # {{context}}
    # {{job}}
    # {{recommendation}}
    return render(request, 'jobber/recommend.html', context)

# Create your views here.

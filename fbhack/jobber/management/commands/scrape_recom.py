from django.core.management import BaseCommand
from bs4 import BeautifulSoup
from jobber.models import Recomendation
from yt_recommender import youtube_search
import requests


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        self.data = []
        self.jobs = ['Therapist', 'Software Developer', 'Chef', 'Sales Engineer', 'Personal trainer']
        self.iterate_through_jobs()

    def iterate_through_jobs(self):
        for job in self.jobs:
            quora = self.get_jobs_from_quora(job)[:6]
            yt = youtube_search(job)[1][:6]
            self.add_to_db(job, quora)
            self.add_to_db(job, yt)
    
    def add_to_db(self, job, data):
        for prof in data:
            
            img = prof.get('img', '')
            recomendation = Recomendation.objects.get_or_create(
                link=prof['link'],
                defaults={
                    'job': job,
                    'type': prof['type'],
                    'title': prof['title'],
                    'content': prof['content'],
                    'img': img,
                }
            )

    def get_jobs_from_quora(self, job):
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
        data = []
        try:
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
            for link in links[:6]:
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
                    'type': 'quora',
                    'link': link,
                    'title': title,
                    'content': text_togheter
                })
        except Exception as e:
            print(e)
            return data    
        return data
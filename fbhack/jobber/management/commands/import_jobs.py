import json

from django.core.management import BaseCommand

from jobber.models import Job


class Command(BaseCommand):

    def add_arguments(self, parser):
         parser.add_argument(
            'file', help='File with jobs')
    
    def handle(self, *args, **kwargs):
        self.file = kwargs['file']
        self.data = []
        with open(self.file, 'r') as jsonfile:
            self.data = json.load(jsonfile)
        self.save_to_db()

    def save_to_db(self):
        i = 0
        tab_len = len(self.data)
        for job in self.data:
            i+=1
            print(f'{i} / {tab_len}')
            # print(job['Job'])
            # print(job['Probability'])
            _, _ = Job.objects.get_or_create(
                job=job['Job'],
                probability=float(job['Probability'])
            )
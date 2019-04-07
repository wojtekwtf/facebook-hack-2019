from django.db import models

# Create your models here.

class Job(models.Model):
    job = models.CharField(max_length=150)
    probability = models.FloatField()

    def __str__(self):
        return f'{self.job} {self.probability}'


class Recomendation(models.Model):
    job = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    link = models.CharField(max_length=3000, null=True)
    title = models.CharField(max_length=1000, null=True)
    content = models.CharField(max_length=20000, null=True)
    img = models.CharField(max_length=3000, null=True)
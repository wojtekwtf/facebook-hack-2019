from django.db import models

# Create your models here.

class Job(models.Model):
    job = models.CharField(max_length=150)
    probability = models.FloatField()

    def __str__(self):
        return f'{self.job} {self.probability}'
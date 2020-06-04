import datetime

from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=2048)
    created_at = models.DateTimeField('date created', default=datetime.datetime.now())

    def __str__(self):
        return self.title

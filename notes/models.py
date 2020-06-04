import datetime

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=2048)
    created_at = models.DateTimeField('date created', default=datetime.datetime.now())
    updated_at = models.DateTimeField('date updated', default=datetime.datetime.now())
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager

from tags.models import TaggedWhatever


class Note(models.Model):
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=20480, blank=True)
    created_at = models.DateTimeField('date created', default=datetime.datetime.now(tz=timezone.utc))
    updated_at = models.DateTimeField('date updated', default=datetime.datetime.now(tz=timezone.utc))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tags = TaggableManager(through=TaggedWhatever, blank=True)

    def __str__(self):
        return self.title


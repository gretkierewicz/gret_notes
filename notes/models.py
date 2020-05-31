from django.db import models


class Note(models.Model):
    body = models.CharField(max_length=500)
    create_time = models.DateTimeField('date created')

    def __str__(self):
        return self.body

from django.db import models


class Event(models.Model):
    title = models.TextField(max_length=128)

from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    title = models.TextField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

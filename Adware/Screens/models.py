from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Screens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    landmarks = models.CharField(max_length=200)


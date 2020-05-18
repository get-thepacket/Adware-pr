from django.db import models
from django.contrib.auth.models import User


class Screens(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.TextField(max_length=100) # will be divided into more fields later
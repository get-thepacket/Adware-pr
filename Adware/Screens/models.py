from django.db import models
import uuid
from django.contrib.auth.models import User


class Screens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    landmarks = models.CharField(max_length=200)


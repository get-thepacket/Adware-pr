from django.db import models
from Advertiser.models import Advertiser

class Screens(models.Model):
    owner_email = models.ForeignKey(Advertiser,on_delete=models.CASCADE)
    location = models.TextField(max_length=100) # will be divided into more fields later
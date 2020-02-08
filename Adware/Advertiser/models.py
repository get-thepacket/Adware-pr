from django.db import models
from django.contrib.auth.models import User


class Advertiser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=10)


class AdMedia(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=30)
    media = models.FileField()



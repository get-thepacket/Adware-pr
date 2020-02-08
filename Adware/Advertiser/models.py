from django.db import models

class Advertiser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=10)
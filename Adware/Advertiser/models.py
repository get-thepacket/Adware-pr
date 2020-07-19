from django.db import models
from django.contrib.auth.models import User
from Screens.models import Screens


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


class DisplaysAd(models.Model):
    screen = models.ForeignKey(Screens, on_delete=models.CASCADE)
    ad = models.ForeignKey(AdMedia, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    gateway_id = models.CharField(max_length=50, default="123456")
    screen = models.ForeignKey(Screens, on_delete=models.CASCADE)
    ad = models.ForeignKey(AdMedia, on_delete=models.CASCADE)
    cost = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=50, default="Transaction Failed")




from django.db import models
import uuid
from django.contrib.auth.models import User


class Screens(models.Model):
    category = (
        ('Big', 'More than X area'),
        ('Medium', 'Between X and Y'),
        ('Small', 'Less than Y')
    )
    auto_id = models.AutoField(primary_key=True)
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(default='Big', choices=category, max_length=10)
    description = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    landmarks = models.CharField(max_length=200)
    ad_available = models.IntegerField(default=20)


class Waitlist(models.Model):
    user_waiting = models.ForeignKey(User, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screens, on_delete=models.CASCADE)


class WaitCount(models.Model):
    screen = models.ForeignKey(Screens, on_delete=models.CASCADE)
    count = models.IntegerField()


class ScreenStats(models.Model):
    screen = models.ForeignKey(Screens, on_delete=models.CASCADE)
    queue = models.BinaryField()
    sum = models.IntegerField(default=0)


class ScreenCost(models.Model):
    screen = models.ForeignKey(Screens, on_delete=models.CASCADE)
    cost = models.IntegerField(editable=True)



from django.db import models
from django.contrib.auth.models import User

choices = (
    ('adv', 'Advertiser'),
    ('scr', 'Screen')
)


class AppUser(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=choices, default='adv')

    # More fields may be added in future

    class Meta:
        unique_together = (('User', 'type'),)

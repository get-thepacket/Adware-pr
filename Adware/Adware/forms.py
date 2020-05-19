from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm(UserCreationForm):
    type = forms.CharField(max_length=10)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ]

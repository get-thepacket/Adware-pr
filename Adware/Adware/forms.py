from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


choices = (
    ('Advertiser','Advertiser'),
    ('Vendor', 'Vendor')
)

class UserForm(UserCreationForm):
    type = forms.ChoiceField(choices=choices)
    class Meta:

        model = User
        fields = ['first_name', 'last_name', 'email' ]

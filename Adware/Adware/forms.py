from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

choices = (
    ('Advertiser', 'Advertiser'),
    ('Vendor', 'Vendor')
)


class UserForm(UserCreationForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
    type = forms.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

from django import forms
from .models import Screens


class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screens
        fields = ('description', 'address', 'landmarks')

from django import forms
from .models import AdMedia


class AdMediaForm(forms.ModelForm):
    class Meta:
        model = AdMedia
        fields = {'file_name', 'media'}

from django import forms
from .models import AdMedia


class AdMediaForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['file_name'].widget.attrs.update({'class':'form-control'})
        self.fields['media'].widget.attrs.update({'class':'form-control'})


    class Meta:
        model = AdMedia
        fields = {'file_name', 'media'}

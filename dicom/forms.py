from django import forms
from .models import DicomImages


class FileForm(forms.ModelForm):
    label = ''

    class Meta:
        model = DicomImages
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True})
        }

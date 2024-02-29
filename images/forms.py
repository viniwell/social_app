from typing import Any
from django import forms
from django.utils.text import slugify
from .models import Image
import requests
from django.core.files.base import ContentFile

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['title', 'url', 'description']
        widgets={
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url=self.cleaned_data['url']
        valid_extentions=['jpg', 'jpeg', 'png']
        extention=url.split('.')[-1].lower()
        if extention not in valid_extentions:
            raise forms.ValidationError('The provided url has invalid extention')
        else:
            return url
        
    def save(self, commit = True):
        image = super().save(commit=False)
        image_url=self.cleaned_data['url']
        name=slugify(image.title)
        extention=image_url.split('.')[-1]
        image_name=f'{name}.{extention}'
        responce=requests.get(image_url)
        image.image.save(image_name, ContentFile(responce.content), save=False)
        if commit:
            image.save()
        return image

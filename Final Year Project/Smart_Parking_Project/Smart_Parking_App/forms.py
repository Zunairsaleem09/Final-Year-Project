from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.widgets import FileInput

class ProductForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Post Title"}))
    thumbnail = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"description"}))
    price = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"price"}))
    location = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Location"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Phone NO"}))
    class Meta:
        model = Product
        exclude = ['vendor']


class ImageForm(ModelForm):
    images = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control", "multiple":True}))
    class Meta:
        model = Image
        fields = ['images']

class ProfileForm(ModelForm):
    class Meta:
        model = profile_edit
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_img': FileInput(),
        }
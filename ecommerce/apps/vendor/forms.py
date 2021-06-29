from django.forms import ModelForm
from apps.product.models import Product
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from django.contrib.auth.models import Group

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields=['category','image','title','description','price']



class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        
        user.save()
        return user
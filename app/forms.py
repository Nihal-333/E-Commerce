from django import forms
from django.contrib.auth.models import User
from .models import Adrs, Customer

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'addres', 'city', 'pincode', 'state']
        widgets = {

            'name': forms.TextInput(attrs={'class':'form-control'}),
            'addres': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'pincode': forms.NumberInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'form-control'})

        }

class CustomerAdrsForm(forms.ModelForm):
    class Meta:
        model = Adrs
        fields = ['name', 'addres', 'city', 'pincode', 'state']
        widgets = {

            'name': forms.TextInput(attrs={'class':'form-control'}),
            'addres': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'pincode': forms.NumberInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'form-control'})

        }

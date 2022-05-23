from django import forms
from django.forms import TextInput

from cities.models import City


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название города'})
        }
        labels = {
            'name': "Город"
        }

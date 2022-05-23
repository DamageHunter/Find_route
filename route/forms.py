from django import forms
from cities.models import City

from route.models import Route


# Users input form
class FindRouteForm(forms.Form):
    queryset = City.objects.all()

    from_city = forms.ModelChoiceField(
        queryset=queryset,
        widget=forms.Select(attrs={'class': 'js-example-basic-single '}),
        label='Город отправления',
        empty_label='Выберите город отправления', )

    to_city = forms.ModelChoiceField(
        queryset=queryset,
        widget=forms.Select(attrs={'class': 'js-example-basic-single '}),
        label='Город назначения',
        empty_label='Выберите город назначения')

    cities = forms.ModelMultipleChoiceField(
        queryset=queryset,
        widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple '}),
        required=False,
        label='Через города:')

    time = forms.IntegerField(
        max_value=10000,
        widget=forms.NumberInput(attrs={'placeholder': 'Введите время в пути'}),
        label='Время в пути')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_value in self.fields.items():
            if field_value.widget.attrs.get('class'):
                field_value.widget.attrs['class'] += 'form-control'
            else:
                field_value.widget.attrs.update({'class': 'form-control'})


# form for saving route
class SaveRouteForm(forms.ModelForm):
    name = forms.CharField(
        label="Введите название маршрута",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'unique': 'Маршрут с таким названием уже существует'}
    )

    class Meta:
        model = Route
        fields = '__all__'
        widgets = {
            'name': forms.HiddenInput(),
            'from_city': forms.HiddenInput(),
            'to_city': forms.HiddenInput(),
            'travel_time': forms.HiddenInput(),
            'trains': forms.MultipleHiddenInput()
        }

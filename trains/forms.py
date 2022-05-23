from django import forms

from trains.models import Train


class TrainForm(forms.ModelForm):

    class Meta:
        model = Train
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control col-3'

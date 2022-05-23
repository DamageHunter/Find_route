from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from cities.models import City


# Create your models here.
class Train(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Номер поезда')

    travel_time = models.PositiveSmallIntegerField(
        verbose_name='Время в пути')

    from_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='from_city',
        verbose_name='Из какого города', db_index=True)

    to_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='to_city',
        verbose_name='В какой город',
        db_index=True)

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезды'
        ordering = ['travel_time']

    def __str__(self):
        return f'Поезд № {self.name} из города {self.from_city}'

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Города прибытия у убытия совпадают')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('trains:train-info', kwargs={'pk': self.id})

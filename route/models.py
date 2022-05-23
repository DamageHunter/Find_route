from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from cities.models import City
from trains.models import Train


class Route(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Города',
        unique=True
    )

    from_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='routes_from_city',
        verbose_name='Из какого города',
    )

    to_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='routes_to_city',
        verbose_name='В какой город',
    )

    trains = models.ManyToManyField(
        Train,
        verbose_name='Список поездов'
    )

    travel_time = models.PositiveSmallIntegerField(
        verbose_name='Время в пути'
    )

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['travel_time']

    def __str__(self):
        return f"Маршрут из города {self.from_city}"

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Города прибытия и убытия совпадают')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('route:route_info', kwargs={'pk': self.id})




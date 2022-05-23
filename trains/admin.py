from django.contrib import admin

from trains.models import Train


# Register your models here.


@admin.register(Train)
class TrainsAdmin(admin.ModelAdmin):
    list_display = ['name', 'travel_time', 'from_city', 'to_city']
    list_editable = ['travel_time']

    class Meta:
        model = Train

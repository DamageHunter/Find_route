from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from route.models import Route


# Register your models here.
@admin.register(Route)
class ForModelAdmin(admin.ModelAdmin):
    pass


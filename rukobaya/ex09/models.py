from django.db import models

# Create your models here.
from django.db import models

class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    climate = models.CharField(max_length=255, null=True, blank=True)
    diameter = models.IntegerField(null=True, blank=True)
    orbital_period = models.IntegerField(null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    rotation_period = models.IntegerField(null=True, blank=True)
    surface_water = models.FloatField(null=True, blank=True)
    terrain = models.CharField(max_length=128, null=True, blank=True)

    # Automatically set to current timestamp
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    birth_year = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)
    eye_color = models.CharField(max_length=32, blank=True, null=True)
    hair_color = models.CharField(max_length=32, blank=True, null=True)
    height = models.IntegerField(null=True, blank=True)
    mass = models.FloatField(null=True, blank=True)

    # homeworld を name ではなく、Planets の id (pk) として参照する場合
    #  to_field や db_column は使わず、通常の ForeignKey でOK
    homeworld = models.ForeignKey(
        'Planets',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

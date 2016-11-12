from __future__ import unicode_literals

from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, related_name='models')

    def __str__(self):
        return self.name


class CarType(models.Model):
    name = models.CharField(max_length=128)
    car_model = models.ForeignKey(CarModel, related_name='types')

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    car_type = models.ForeignKey(CarType, related_name='cars')

    def __str__(self):
        return self.name


class SpecificationCategory(models.Model):
    name = models.CharField(max_length=128)
    car = models.ForeignKey(Car, related_name='categories', null=True, blank=True)

    def __str__(self):
        return self.name


class Specification(models.Model):
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    category = models.ForeignKey(SpecificationCategory, related_name='specifications')
    car = models.ForeignKey(Car, related_name='specifications')

    def __str__(self):
        return self.name



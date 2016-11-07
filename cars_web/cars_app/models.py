from __future__ import unicode_literals

from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=128)


class CarModel(models.Model):
    name = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand)


class CarType(models.Model):
    name = models.CharField(max_length=128)
    car_model = models.ForeignKey(CarModel)


class Car(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=512)
    car_type = models.ForeignKey(CarType)


class SpecificationCategory(models.Model):
    name = models.CharField(max_length=128)
    car = models.ForeignKey(Car, null=True, blank=True)


class Specification(models.Model):
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    category = models.ForeignKey(SpecificationCategory)
    car = models.ForeignKey(Car)



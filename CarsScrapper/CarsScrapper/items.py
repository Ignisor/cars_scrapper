# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from CarsApp.models import Brand, CarModel, CarType, Car, Specification, SpecificationCategory


class BrandItem(DjangoItem):
    django_model = Brand


class CarModelItem(DjangoItem):
    django_model = CarModel


class CarTypeItem(DjangoItem):
    django_model = CarType


class CarItem(DjangoItem):
    django_model = Car


class SpecificationItem(DjangoItem):
    django_model = Specification


class SpecificationCategoryItem(DjangoItem):
    django_model = SpecificationCategory

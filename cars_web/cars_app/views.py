from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets

from .models import Brand, CarModel, CarType, Car, Specification, SpecificationCategory
from .serializers import BrandSerializer, CarModelSerializer, CarTypeSerializer, \
    CarSerializer, SpecificationCategorySerializer, SpecificationSerializer
from rest_framework.response import Response

# shows list of brands
def index(request):
    brands_list = Brand.objects.order_by('name')
    context = {
        'brands_list':brands_list
    }

    return render(request, 'index.html', context)


# shows all models of brand
def models(request, brand_name):
    brand = get_object_or_404(Brand, name = brand_name)
    models_list = brand.models.order_by('name')
    context = {
        'models_list':models_list,
        'brand_name':brand_name
    }

    return render(request, 'models.html', context)


# shows all types of model
def types(request, brand_name, model_name):
    model = get_object_or_404(CarModel, name = model_name)
    types_list = model.types.order_by('name')
    context = {
        'types_list':types_list,
        'model_name':model_name,
    }

    return render(request, 'types.html', context)


# shows all cars of type
def cars(request, brand_name, model_name, type_name):
    type = get_object_or_404(CarType, name = type_name)
    cars_list = type.cars.order_by('name')
    context = {
        'cars_list':cars_list,
        'type_name':type_name,
    }

    return render(request, 'cars.html', context)


# shows car data
def car(request, brand_name, model_name, type_name, car_name):
    car = get_object_or_404(Car, name = car_name)
    context = {
        'car': car,
        'car_name': car_name,
    }

    return render(request, 'car.html', context)


#REST API
class BrandViewSet(viewsets.ModelViewSet):
    """
    Allows to edit and view Brands
    """
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    """
    Allows to edit and view CarModels
    """
    queryset = CarModel.objects.all().order_by('name')
    serializer_class = CarModelSerializer


class CarTypeViewSet(viewsets.ModelViewSet):
    """
    Allows to edit and view CarTypes
    """
    queryset = CarType.objects.all().order_by('name')
    serializer_class = CarTypeSerializer


class CarViewSet(viewsets.ModelViewSet):
    """
    Allows to edit and view Cars
    """
    queryset = Car.objects.all().order_by('name')
    serializer_class = CarSerializer


class SpecificationCategoryViewSet(viewsets.ModelViewSet):
    """
    Allows to edit and view SpecificationCategories
    """
    queryset = SpecificationCategory.objects.all()
    serializer_class = SpecificationCategorySerializer

    def list(self, request, *args, **kwargs):
        return Response('List view is disabled. Get category by it\'s id')


class SpecificationViewSet(viewsets.ModelViewSet):
    """
    Allows to edit and view Specification
    """
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

    def list(self, request, *args, **kwargs):
        return Response('List view is disabled. Get specification by it\'s id')


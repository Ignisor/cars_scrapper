from django.conf.urls import url
from . import views

urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),
    # Brand/
    url(r'^(?P<brand_name>[\w -.]+)/$', views.models, name='models'),
    # Brand/Model/
    url(r'^(?P<brand_name>[\w -.]+)/(?P<model_name>[\w -.]+)/$', views.types, name='types'),
    # Brand/Model/Type/
    url(r'^(?P<brand_name>[\w -.]+)/(?P<model_name>[\w -.]+)/(?P<type_name>[\w -.]+)/$', views.cars, name='cars'),
    # Brand/Model/Type/Car/
    url(r'^(?P<brand_name>[\w -.]+)/(?P<model_name>[\w -.]+)/(?P<type_name>[\w -.]+)/(?P<car_name>[\w -.]+)/$', views.car, name='car'),
]
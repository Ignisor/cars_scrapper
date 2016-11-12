from .models import Brand, CarModel, CarType, Car, Specification, SpecificationCategory
from rest_framework import serializers


# serializer for 'Brand' model
class BrandSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=128, required=True)
    models = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """
        create and return new 'Brand' instance
        """
        new_brand = Brand(name=validated_data.get('name'),)
        new_brand.save()

        return new_brand

    def update(self, instance, validated_data):
        """
        Update and return an existing `Brand` instance
        """
        instance.name = validated_data.get('name', instance.name)

        instance.save()
        return instance


# serializer for 'CarModel' model
class CarModelSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=128, required=True)
    brand = serializers.PrimaryKeyRelatedField(required=True, queryset=Brand.objects.all())
    types = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """
        create and return new 'CarModel' instance
        """
        new_model = CarModel(name=validated_data.get('name'),
                          brand=validated_data.get('brand'), )
        new_model.save()

        return new_model

    def update(self, instance, validated_data):
        """
        Update and return an existing `CarModel` instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.brand = validated_data.get('brand', instance.brand)

        instance.save()
        return instance


# serializer for 'CarType' model
class CarTypeSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=128, required=True)
    car_model = serializers.PrimaryKeyRelatedField(required=True, queryset=CarModel.objects.all())
    cars = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """
        create and return new 'CarType' instance
        """
        new_type = CarType(name=validated_data.get('name'),
                          car_model=validated_data.get('car_model'),)
        new_type.save()

        return new_type

    def update(self, instance, validated_data):
        """
        Update and return an existing `CarType` instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.car_model = validated_data.get('car_model', instance.car_model)

        instance.save()
        return instance


# serializer for 'Car' model
class CarSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=128, default='NoName')
    url = serializers.CharField(max_length=512, required=True)
    car_type = serializers.PrimaryKeyRelatedField(required=True, queryset=CarType.objects.all())
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """
        create and return new 'Car' instance
        """
        new_car = Car(name = validated_data.get('name'),
                      url = validated_data.get('url'),
                      car_type = validated_data.get('car_type'))
        new_car.save()

        return new_car

    def update(self, instance, validated_data):
        """
        Update and return an existing `Car` instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.car_type = validated_data.get('car_type', instance.car_type)

        instance.save()
        return instance


# serializer for 'SpecificationCategory' model
class SpecificationCategorySerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=128, required=True)
    car = serializers.PrimaryKeyRelatedField(required=True, queryset=Car.objects.all())
    specifications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """
        create and return new 'SpecificationCategory' instance
        """
        new_category = SpecificationCategory(name = validated_data.get('name'),
                                             car = validated_data.get('car'),)
        new_category.save()

        return new_category

    def update(self, instance, validated_data):
        """
        Update and return an existing `SpecificationCategory` instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.car = validated_data.get('car', instance.car)

        instance.save()
        return instance


# serializer for 'Specification' model
class SpecificationSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    key = serializers.CharField(max_length=128, required=True)
    value = serializers.CharField(max_length=128, allow_blank=True, allow_null=True)
    car = serializers.PrimaryKeyRelatedField(required=True, queryset=Car.objects.all())
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=SpecificationCategory.objects.all())

    def create(self, validated_data):
        """
        create and return new 'Specification' instance
        """
        new_spec = Specification(key = validated_data.get('key'),
                                 value = validated_data.get('value'),
                                 category = validated_data.get('category'),
                                 car = validated_data.get('car'),)
        new_spec.save()

        return new_spec

    def update(self, instance, validated_data):
        """
        Update and return an existing `Specification` instance
        """
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.category = validated_data.get('category', instance.category)
        instance.car = validated_data.get('car', instance.car)

        instance.save()
        return instance
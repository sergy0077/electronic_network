from rest_framework import serializers
from .models import NetworkObject, Product, Factory, RetailNetwork, Entrepreneur, Supplier


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkObjectSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkObject
        fields = '__all__'


class FactorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Factory
        fields = '__all__'


class RetailNetworkSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = RetailNetwork
        fields = '__all__'


class EntrepreneurSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Entrepreneur
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    """
    Запретили обновление через API поля «Задолженность перед поставщиком»);
    """
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('debt_to_supplier',)  # Запрещаем обновление поля "Задолженность перед поставщиком"

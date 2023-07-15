from rest_framework import serializers

from . import models


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    quantity = serializers.IntegerField()
    cost = serializers.DecimalField(max_digits=5, decimal_places=2)


class OrderSerializer(serializers.Serializer):
    point_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    items = serializers.ListField(child=ProductSerializer())


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Check
        fields = ('printer_id', 'type', 'order', 'status', 'pdf_file')

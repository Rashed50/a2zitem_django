from rest_framework import serializers

##? Models Import
from apps.sales.models.sale import Customer


class CustomerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Customer
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'address',
        ]
from rest_framework import serializers

##? Models Import
from core.models.address_model import Country, State, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Country
        fields = ('id', 'name', 'code')


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = State
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = City
        fields = ('id', 'name')
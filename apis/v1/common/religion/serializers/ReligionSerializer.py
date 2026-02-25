from rest_framework import serializers

##? Models Import
from core.models.religion_model import Religion

class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Religion
        fields = ['id', 'name']
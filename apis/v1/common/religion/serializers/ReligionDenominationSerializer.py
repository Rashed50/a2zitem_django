from rest_framework import serializers

##? Models Import
from core.models.religion_model import ReligionDenomination

class ReligionDenominationSerializer(serializers.ModelSerializer):
    religion_id   = serializers.PrimaryKeyRelatedField(source='religion', read_only=True)
    religion_name = serializers.CharField(source='religion.name', read_only=True)
    
    class Meta:
        model  = ReligionDenomination
        fields = ['id', 'name' , 'religion_id', 'religion_name']
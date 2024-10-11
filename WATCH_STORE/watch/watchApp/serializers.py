from .models import Web
from rest_framework import serializers

class WebSerializer(serializers.ModelSerializer):
    name=serializers.CharField(max_length=200,required=True)
    email=serializers.CharField(max_length=200,required=True)

    class Meta:
        model = Web
        fields = ("__all__")

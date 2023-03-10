from rest_framework import serializers
from gadgets.models import (Device)
from accounts.serializers import CompanySerializer


class DeviceSerializer(serializers.ModelSerializer):
    owner = CompanySerializer(required=False)

    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data["name"]
        type = validated_data["type"]
        company_id = validated_data["company_id"]

        return Device.objects.create(name=name, type=type, owner_id=company_id)

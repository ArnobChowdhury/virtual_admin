from rest_framework import serializers
from gadgets.models import (Device, Requisition)
from accounts.serializers import CompanySerializer, EmployeeSerializer


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


class RequisitionSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(required=False)
    requested_by = EmployeeSerializer(required=False)
    reviewed_by = EmployeeSerializer(required=False)

    class Meta:
        model = Requisition
        fields = '__all__'

    def create(self, validated_data):
        device_id = validated_data["device_id"]
        requested_by_id = validated_data["requested_by_id"]
        requested_checkout_date = validated_data["requested_checkout_date"]
        requested_return_date = validated_data["requested_return_date"]
        reason = validated_data["reason"]

        # only the fields required for making an application
        return Requisition.objects.create(device_id=device_id, requested_by_id=requested_by_id,
                                          requested_checkout_date=requested_checkout_date,
                                          requested_return_date=requested_return_date, reason=reason)

from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import (Company, Employee)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        return User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(required=False)
    user = UserSerializer(required=False)

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        company = validated_data["company"]
        user = validated_data["user"]
        department = validated_data["department"]
        designation = validated_data["designation"]
        is_admin = validated_data.get("is_admin", False)
        return Employee.objects.create(department=department, designation=designation,
                                       company_id=company.id, user_id=user.id, is_admin=is_admin)


class CreateCompanySerializer(serializers.Serializer):
    company = CompanySerializer()
    admin = EmployeeSerializer()

    def create(self, validated_data):
        company = validated_data["company"]
        company = Company.objects.create(**company)

        employee = validated_data["admin"]
        department = employee["department"]
        designation = employee["designation"]

        user = validated_data["user"]
        Employee.objects.update_or_create(user_id=user.id, defaults={
            'department': department, 'designation': designation,
            "company_id": company.id, "is_admin": True})

        return {"company": company, "admin": employee}

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret["company"]

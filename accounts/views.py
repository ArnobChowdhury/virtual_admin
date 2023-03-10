from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer, CreateCompanySerializer, EmployeeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCompanyAdmin
from django.contrib.auth.models import User


class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class CreateCompanView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class AddEmployee(APIView):
    permission_classes = [IsCompanyAdmin]

    def post(self, request):
        company = request.user.employee.company
        user_id = request.data["user_id"]

        try:
            user = User.objects.get(id=user_id)
            if hasattr(user, 'employee'):
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"detail": "Already an employee of this company"})

        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': f"An user with user id {user_id} does not exist"})

        employee_serializer = EmployeeSerializer(data=request.data)
        employee_serializer.is_valid(raise_exception=True)
        employee_serializer.save(user=user, company=company)

        return Response(status=status.HTTP_201_CREATED, data=employee_serializer.data)

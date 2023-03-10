from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer, CreateCompanySerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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

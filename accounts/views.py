from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from rest_framework import status


class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

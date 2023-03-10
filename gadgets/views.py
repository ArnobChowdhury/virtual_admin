from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from gadgets.models import Device
from gadgets.serializers import DeviceSerializer
from gadgets.permissions import ReadOnlyForAuthenticated
from accounts.permissions import IsCompanyAdmin


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCompanyAdmin | ReadOnlyForAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()

    def create(self, request, *args, **kwargs):
        company_id = self.request.user.employee.company.id
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company_id=company_id)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

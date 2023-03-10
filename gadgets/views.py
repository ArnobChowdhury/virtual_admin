from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from gadgets.models import Device, Requisition
from gadgets.serializers import DeviceSerializer, RequisitionSerializer
from gadgets.permissions import ReadOnlyForAuthenticated
from accounts.permissions import IsCompanyAdmin
import datetime


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


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RequisitionSerializer
    queryset = Requisition.objects.all()

    def create(self, request, *args, **kwargs):
        requested_by_id = request.user.employee.id
        device_id = request.data.get("device_id")
        serializer = RequisitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(requested_by_id=requested_by_id, device_id=device_id)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def update_status(self, request, requisition_status):
        requisition = self.get_object()
        requisition.status = requisition_status
        requisition.reviewed_by_id = request.user.employee.id
        requisition.save()
        serializer = self.get_serializer(requisition)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsCompanyAdmin])
    def approve(self, request, pk=None):
        return self.update_status(request, "APR")

    @action(detail=True, methods=['post'], permission_classes=[IsCompanyAdmin])
    def reject(self, request, pk=None):
        return self.update_status(request, "REJ")

    @action(detail=True, methods=['post'])
    def device_checkout(self, request, pk=None):
        requisition = self.get_object()

        condition = None
        try:
            last_requisition = Requisition.objects.filter(device_id=requisition.device_id, actual_checkout_date__isnull=False) \
                .exclude(id=requisition.id) \
                .latest('actual_checkout_date')
            if last_requisition.status != "RET":
                return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Device not available at the moment"})
            # condition of the device is the last return condition of the device
            condition = last_requisition.return_condition
        except Requisition.DoesNotExist:
            condition = 'OK'
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        checkout_requester = request.user.employee
        requisition_requested_by = requisition.requested_by
        requisition_is_approved = requisition.status == 'APR'
        checkout_by_other = checkout_requester != requisition_requested_by

        if not requisition_is_approved or checkout_by_other:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You cannot check this device out"})

        requisition.actual_checkout_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        requisition.checkout_condition = condition
        requisition.status = "OUT"
        requisition.save()

        serializer = self.get_serializer(requisition)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(detail=True, methods=['post'])
    def device_return(self, request, pk=None):
        requisition = self.get_object()
        return_requester = request.user.employee
        requisition_requested_by = requisition.requested_by
        device_is_handed_out = requisition.status == 'OUT'
        return_by_other = return_requester != requisition_requested_by

        if not device_is_handed_out or return_by_other:
            return Response(status=status.HTTP_403_FORBIDDEN)

        requisition.actual_return_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        condition = request.data["condition"]

        requisition.return_condition = condition
        requisition.status = "RET"
        requisition.save()

        serializer = self.get_serializer(requisition)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

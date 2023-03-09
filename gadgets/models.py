from django.db.models import (Model, CharField, ForeignKey,
                              CASCADE, DateTimeField, SET_NULL)
from accounts.models import (Company, Employee)


class Device(Model):
    PHONE = "PH"
    TAB = "TAB"
    LAPTOP = "LT"
    DEVICE_TYPE_CHOICES = [
        (PHONE, 'Phone'),
        (TAB, 'Tablet'),
        (LAPTOP, 'Laptop'),
    ]

    name = CharField(max_length=255)
    type = CharField(max_length=3, choices=DEVICE_TYPE_CHOICES)
    owner = ForeignKey(Company, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.type}: {self.name} of {self.owner.name}"


class Requisition(Model):
    REQUESTED = "REQ"
    APPROVED = "APR"
    HANDED_OUT = "OUT"
    REJECTED = "REJ"
    RETURNED = "RET"
    REQUSITION_STATUS = [
        (REQUESTED, 'Requested'),
        (APPROVED, 'Approved'),
        (HANDED_OUT, 'Handed Out'),
        (REJECTED, 'Rejected'),
        (RETURNED, 'Returned'),
    ]

    WORKING = 'OK'
    NEEDS_REPAIR = 'NR'
    DEVICE_CONDITION = [
        (WORKING, 'WORKING'),
        (NEEDS_REPAIR, 'NEEDS REPAIR')
    ]

    device = ForeignKey(Device, on_delete=SET_NULL, null=True)
    requested_by = ForeignKey(Employee, on_delete=SET_NULL, null=True, related_name='device_requested')
    reviewed_by = ForeignKey(Employee, on_delete=SET_NULL, blank=True, null=True,
                             related_name='device_requisition_reviewed')
    status = CharField(max_length=3, choices=REQUSITION_STATUS, default=REQUESTED)

    checkout_condition = CharField(max_length=2, choices=DEVICE_CONDITION, blank=True, null=True)
    return_condition = CharField(max_length=3, choices=DEVICE_CONDITION, blank=True, null=True)

    requested_checkout_date = DateTimeField()
    requested_return_date = DateTimeField()

    actual_checkout_date = DateTimeField(blank=True, null=True)
    actual_return_date = DateTimeField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.requested_by.user.username}, {self.requested_by.department} {self.requested_by.designation}, {self.requested_by.company.name} for {self.device.name}"

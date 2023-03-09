from django.contrib.auth.models import User
from django.db.models import (Model, CharField, ForeignKey, CASCADE, OneToOneField)


class Company(Model):
    name = CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Employee(Model):
    department = CharField(max_length=255)
    designation = CharField(max_length=255)
    company = ForeignKey(Company, on_delete=CASCADE, related_name="company")
    user = OneToOneField(User, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}, {self.department} {self.designation}, {self.company.name}"

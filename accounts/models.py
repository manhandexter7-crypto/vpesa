import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(max_length=150)

    kyc_status = models.CharField(
        max_length=30,
        choices=[
            ("PENDING", "Pending"),
            ("VERIFIED", "Verified"),
            ("REJECTED", "Rejected"),
        ],
        default="PENDING"
    )

    account_status = models.CharField(
        max_length=30,
        choices=[
            ("ACTIVE", "Active"),
            ("LOCKED", "Locked"),
            ("SUSPENDED", "Suspended"),
        ],
        default="ACTIVE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"
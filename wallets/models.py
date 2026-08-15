import uuid

from django.conf import settings
from django.db import models


class Wallet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="wallet"
    )

    currency = models.CharField(
        max_length=3,
        default="KES"
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("ACTIVE", "Active"),
            ("FROZEN", "Frozen"),
            ("CLOSED", "Closed"),
        ],
        default="ACTIVE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.currency}"
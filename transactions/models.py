import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models


class Transaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REVERSED", "Reversed"),
    ]

    TYPE_CHOICES = [
        ("TRANSFER", "Transfer"),
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("REFUND", "Refund"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    idempotency_key = models.CharField(
        max_length=100,
        unique=True
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        default="KES"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="sent_transactions"
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="received_transactions"
    )

    provider = models.CharField(
        max_length=50,
        blank=True
    )

    provider_reference = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.reference


class LedgerAccount(models.Model):

    ACCOUNT_TYPES = [
        ("ASSET", "Asset"),
        ("LIABILITY", "Liability"),
        ("EQUITY", "Equity"),
        ("REVENUE", "Revenue"),
        ("EXPENSE", "Expense"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES
    )

    currency = models.CharField(
        max_length=3,
        default="KES"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class LedgerEntry(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name="ledger_entries"
    )

    account = models.ForeignKey(
        LedgerAccount,
        on_delete=models.PROTECT,
        related_name="entries"
    )

    debit = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00")
    )

    credit = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00")
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(debit__gte=0)
                    & models.Q(credit__gte=0)
                ),
                name="non_negative_ledger_values"
            )
        ]
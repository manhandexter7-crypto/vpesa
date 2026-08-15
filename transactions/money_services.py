from decimal import Decimal

from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import (
    Transaction,
    LedgerEntry,
)

from .services import (
    get_user_ledger_account,
    get_system_account,
)


@db_transaction.atomic
def create_sandbox_deposit(
    user,
    amount,
    idempotency_key
):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValidationError(
            "Deposit amount must be greater than zero."
        )

    existing = Transaction.objects.filter(
        idempotency_key=idempotency_key
    ).first()

    if existing:
        return existing

    user_account = get_user_ledger_account(user)

    sandbox_account = get_system_account(
        "SANDBOX_EXTERNAL_FUNDS"
    )

    tx = Transaction.objects.create(
        reference=f"VPESA-DEP-{timezone.now().strftime('%Y%m%d%H%M%S%f')}",
        idempotency_key=idempotency_key,
        transaction_type="DEPOSIT",
        status="COMPLETED",
        amount=amount,
        currency="KES",
        recipient=user,
        provider="SANDBOX",
        provider_reference=f"TEST-{timezone.now().timestamp()}",
        description="Sandbox deposit",
        completed_at=timezone.now(),
    )

    LedgerEntry.objects.create(
        transaction=tx,
        account=sandbox_account,
        debit=amount,
        credit=Decimal("0.00"),
    )

    LedgerEntry.objects.create(
        transaction=tx,
        account=user_account,
        debit=Decimal("0.00"),
        credit=amount,
    )

    return tx


@db_transaction.atomic
def create_sandbox_withdrawal(
    user,
    amount,
    idempotency_key
):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValidationError(
            "Withdrawal amount must be greater than zero."
        )

    existing = Transaction.objects.filter(
        idempotency_key=idempotency_key
    ).first()

    if existing:
        return existing

    user_account = get_user_ledger_account(user)

    credits = LedgerEntry.objects.filter(
        account=user_account
    ).aggregate(
        total=Sum("credit")
    )["total"] or Decimal("0.00")

    debits = LedgerEntry.objects.filter(
        account=user_account
    ).aggregate(
        total=Sum("debit")
    )["total"] or Decimal("0.00")

    balance = credits - debits

    if balance < amount:
        raise ValidationError(
            "Insufficient VPesa balance."
        )

    external_account = get_system_account(
        "SANDBOX_EXTERNAL_FUNDS"
    )

    tx = Transaction.objects.create(
        reference=f"VPESA-WD-{timezone.now().strftime('%Y%m%d%H%M%S%f')}",
        idempotency_key=idempotency_key,
        transaction_type="WITHDRAWAL",
        status="COMPLETED",
        amount=amount,
        currency="KES",
        sender=user,
        provider="SANDBOX",
        provider_reference=f"TEST-{timezone.now().timestamp()}",
        description="Sandbox withdrawal",
        completed_at=timezone.now(),
    )

    LedgerEntry.objects.create(
        transaction=tx,
        account=user_account,
        debit=amount,
        credit=Decimal("0.00"),
    )

    LedgerEntry.objects.create(
        transaction=tx,
        account=external_account,
        debit=Decimal("0.00"),
        credit=amount,
    )

    return tx
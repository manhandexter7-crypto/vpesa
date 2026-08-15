from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import Sum
from django.utils import timezone
from django.core.exceptions import ValidationError

from accounts.models import User
from wallets.models import Wallet

from .models import (
    Transaction,
    LedgerAccount,
    LedgerEntry,
)


def get_user_ledger_account(user):
    account, _ = LedgerAccount.objects.get_or_create(
        name=f"USER:{user.id}",
        defaults={
            "account_type": "LIABILITY",
            "currency": "KES",
        }
    )

    return account


def get_system_account(name):
    account, _ = LedgerAccount.objects.get_or_create(
        name=name,
        defaults={
            "account_type": "ASSET",
            "currency": "KES",
        }
    )

    return account


def models_sum(field):
    return Sum(field)


def get_wallet_balance(user):
    account = get_user_ledger_account(user)

    credits = LedgerEntry.objects.filter(
        account=account
    ).aggregate(
        total=models_sum("credit")
    )["total"] or Decimal("0.00")

    debits = LedgerEntry.objects.filter(
        account=account
    ).aggregate(
        total=models_sum("debit")
    )["total"] or Decimal("0.00")

    return credits - debits


@db_transaction.atomic
def create_vpesa_transfer(
    sender,
    recipient,
    amount,
    idempotency_key,
    description=""
):

    amount = Decimal(str(amount))

    # Amount must be positive
    if amount <= 0:
        raise ValidationError(
            "Amount must be greater than zero."
        )

    # Prevent sending to yourself
    if sender.id == recipient.id:
        raise ValidationError(
            "You cannot transfer to yourself."
        )

    # Sender must be active
    if sender.account_status != "ACTIVE":
        raise ValidationError(
            "Sender account is not active."
        )

    # Recipient must be active
    if recipient.account_status != "ACTIVE":
        raise ValidationError(
            "Recipient account is not active."
        )

    # No KYC check here.
    # This allows sandbox accounts to transfer
    # regardless of their KYC status.

    # Prevent duplicate requests
    existing = Transaction.objects.filter(
        idempotency_key=idempotency_key
    ).first()

    if existing:
        return existing

    # Make sure both users have wallets
    Wallet.objects.get_or_create(
        user=sender
    )

    Wallet.objects.get_or_create(
        user=recipient
    )

    # Get ledger accounts
    sender_account = get_user_ledger_account(
        sender
    )

    recipient_account = get_user_ledger_account(
        recipient
    )

    # Calculate sender balance
    sender_entries = LedgerEntry.objects.filter(
        account=sender_account
    )

    sender_credits = sender_entries.aggregate(
        total=models_sum("credit")
    )["total"] or Decimal("0.00")

    sender_debits = sender_entries.aggregate(
        total=models_sum("debit")
    )["total"] or Decimal("0.00")

    available_balance = (
        sender_credits -
        sender_debits
    )

    # Prevent overdrawing the wallet
    if available_balance < amount:
        raise ValidationError(
            "Insufficient VPesa balance."
        )

    # Generate transaction reference
    reference = (
        "VPESA-" +
        timezone.now().strftime(
            "%Y%m%d%H%M%S%f"
        )
    )

    # Create transaction
    tx = Transaction.objects.create(
        reference=reference,
        idempotency_key=idempotency_key,
        transaction_type="TRANSFER",
        status="PROCESSING",
        amount=amount,
        currency="KES",
        sender=sender,
        recipient=recipient,
        description=description,
    )

    # Debit sender
    LedgerEntry.objects.create(
        transaction=tx,
        account=sender_account,
        debit=amount,
        credit=Decimal("0.00")
    )

    # Credit recipient
    LedgerEntry.objects.create(
        transaction=tx,
        account=recipient_account,
        debit=Decimal("0.00"),
        credit=amount
    )

    # Complete transaction
    tx.status = "COMPLETED"

    tx.completed_at = timezone.now()

    tx.save(
        update_fields=[
            "status",
            "completed_at"
        ]
    )

    return tx
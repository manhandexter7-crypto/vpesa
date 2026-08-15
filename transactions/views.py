import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LedgerEntry, Transaction
from .serializers import (
    TransferSerializer,
    MoneySerializer,
)
from .services import (
    create_vpesa_transfer,
)
from .money_services import (
    create_sandbox_deposit,
    create_sandbox_withdrawal,
)


User = get_user_model()


class BalanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        from .services import get_user_ledger_account

        account = get_user_ledger_account(
            request.user
        )

        credits = LedgerEntry.objects.filter(
            account=account
        ).aggregate(
            total=Sum("credit")
        )["total"] or 0

        debits = LedgerEntry.objects.filter(
            account=account
        ).aggregate(
            total=Sum("debit")
        )["total"] or 0

        balance = credits - debits

        return Response({
            "currency": "KES",
            "balance": str(balance),
        })


class TransferView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TransferSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        recipient_phone = serializer.validated_data[
            "recipient_phone"
        ]

        try:
            recipient = User.objects.get(
                phone_number=recipient_phone
            )
        except User.DoesNotExist:
            return Response(
                {
                    "error": "Recipient not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            tx = create_vpesa_transfer(
                sender=request.user,
                recipient=recipient,
                amount=serializer.validated_data["amount"],
                idempotency_key=(
                    request.headers.get(
                        "Idempotency-Key",
                        str(uuid.uuid4())
                    )
                ),
                description=serializer.validated_data.get(
                    "description",
                    ""
                ),
            )

            return Response({
                "reference": tx.reference,
                "status": tx.status,
                "amount": str(tx.amount),
                "recipient": recipient.phone_number,
            })

        except ValidationError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class SandboxDepositView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = MoneySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        key = request.headers.get(
            "Idempotency-Key",
            str(uuid.uuid4())
        )

        try:

            tx = create_sandbox_deposit(
                request.user,
                serializer.validated_data["amount"],
                key
            )

            return Response({
                "reference": tx.reference,
                "status": tx.status,
                "amount": str(tx.amount),
                "provider": "SANDBOX",
            })

        except ValidationError as error:

            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SandboxWithdrawalView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = MoneySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        key = request.headers.get(
            "Idempotency-Key",
            str(uuid.uuid4())
        )

        try:

            tx = create_sandbox_withdrawal(
                request.user,
                serializer.validated_data["amount"],
                key
            )

            return Response({
                "reference": tx.reference,
                "status": tx.status,
                "amount": str(tx.amount),
                "provider": "SANDBOX",
            })

        except ValidationError as error:

            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )


class TransactionHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        transactions = Transaction.objects.filter(
            sender=request.user
        ) | Transaction.objects.filter(
            recipient=request.user
        )

        transactions = transactions.order_by(
            "-created_at"
        )[:100]

        data = []

        for tx in transactions:

            data.append({
                "reference": tx.reference,
                "type": tx.transaction_type,
                "status": tx.status,
                "amount": str(tx.amount),
                "currency": tx.currency,
                "created_at": tx.created_at,
                "description": tx.description,
            })

        return Response(data)
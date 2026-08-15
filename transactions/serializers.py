from rest_framework import serializers

from .models import Transaction


class TransferSerializer(serializers.Serializer):

    recipient_phone = serializers.CharField(
        max_length=20
    )

    amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0.01
    )

    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True
    )


class MoneySerializer(serializers.Serializer):

    amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0.01
    )
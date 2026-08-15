import os

import requests

from .base import PaymentProvider


class MpesaProvider(PaymentProvider):

    def __init__(self):

        self.base_url = os.getenv(
            "MPESA_BASE_URL",
            ""
        )

        self.consumer_key = os.getenv(
            "MPESA_CONSUMER_KEY",
            ""
        )

        self.consumer_secret = os.getenv(
            "MPESA_CONSUMER_SECRET",
            ""
        )

    def initiate_collection(
        self,
        phone_number,
        amount,
        reference
    ):

        if not self.base_url:
            raise RuntimeError(
                "M-Pesa provider endpoint has not been configured."
            )

        # Implement the currently approved
        # Daraja sandbox/production API flow here
        # using credentials supplied by Safaricom.

        raise NotImplementedError(
            "Configure the approved Daraja integration "
            "before enabling provider transactions."
        )

    def initiate_disbursement(
        self,
        phone_number,
        amount,
        reference
    ):

        raise NotImplementedError(
            "Configure the approved Daraja integration "
            "before enabling provider transactions."
        )

    def verify_transaction(
        self,
        provider_reference
    ):

        raise NotImplementedError(
            "Configure the approved Daraja integration "
            "before enabling provider transactions."
        )
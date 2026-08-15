import os

from .base import PaymentProvider


class AirtelMoneyProvider(PaymentProvider):

    def __init__(self):

        self.base_url = os.getenv(
            "AIRTEL_BASE_URL",
            ""
        )

        self.client_id = os.getenv(
            "AIRTEL_CLIENT_ID",
            ""
        )

        self.client_secret = os.getenv(
            "AIRTEL_CLIENT_SECRET",
            ""
        )

    def initiate_collection(
        self,
        phone_number,
        amount,
        reference
    ):

        raise NotImplementedError(
            "Configure the approved Airtel Money "
            "developer integration before enabling provider transactions."
        )

    def initiate_disbursement(
        self,
        phone_number,
        amount,
        reference
    ):

        raise NotImplementedError(
            "Configure the approved Airtel Money "
            "developer integration before enabling provider transactions."
        )

    def verify_transaction(
        self,
        provider_reference
    ):

        raise NotImplementedError(
            "Configure the approved Airtel Money "
            "developer integration before enabling provider transactions."
        )
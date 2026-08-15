from abc import ABC, abstractmethod


class PaymentProvider(ABC):

    @abstractmethod
    def initiate_collection(
        self,
        phone_number,
        amount,
        reference
    ):
        raise NotImplementedError

    @abstractmethod
    def initiate_disbursement(
        self,
        phone_number,
        amount,
        reference
    ):
        raise NotImplementedError

    @abstractmethod
    def verify_transaction(
        self,
        provider_reference
    ):
        raise NotImplementedError
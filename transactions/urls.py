from django.urls import path

from .views import (
    BalanceView,
    TransferView,
    SandboxDepositView,
    SandboxWithdrawalView,
    TransactionHistoryView,
)


urlpatterns = [

    path(
        "balance/",
        BalanceView.as_view()
    ),

    path(
        "transfer/",
        TransferView.as_view()
    ),

    path(
        "deposit/",
        SandboxDepositView.as_view()
    ),

    path(
        "withdraw/",
        SandboxWithdrawalView.as_view()
    ),

    path(
        "history/",
        TransactionHistoryView.as_view()
    ),
]
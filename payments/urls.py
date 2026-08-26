from django.urls import path
from .views import airtel_disbursement_callback

urlpatterns = [
    path(
        "airtel/disbursement/callback/",
        airtel_disbursement_callback,
        name="airtel-disbursement-callback",
    ),
]
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class VPesaUserAdmin(UserAdmin):
    list_display = (
        "username",
        "phone_number",
        "full_name",
        "kyc_status",
        "account_status",
        "created_at",
    )

    list_filter = (
        "kyc_status",
        "account_status",
    )

    search_fields = (
        "username",
        "phone_number",
        "full_name",
    )
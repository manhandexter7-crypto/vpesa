from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .web_views import (
    dashboard,
    login_page,
    register_page,
)


def home(request):
    from django.shortcuts import redirect
    return redirect("/login/")


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        home,
        name="home"
    ),

    path(
        "login/",
        login_page,
        name="login"
    ),

    path(
        "register/",
        register_page,
        name="register"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),

    path(
        "api/auth/",
        include("accounts.urls")
    ),

    path(
        "api/token/",
        TokenObtainPairView.as_view()
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view()
    ),

    path(
        "api/transactions/",
        include("transactions.urls")
    ),
]
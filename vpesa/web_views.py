from django.shortcuts import render


def dashboard(request):
    return render(
        request,
        "vpesa/dashboard.html"
    )


def login_page(request):
    return render(
        request,
        "registration/login.html"
    )


def register_page(request):
    return render(
        request,
        "vpesa/register.html"
    )
from django.shortcuts import render


def login_view(request):
    return render(request, "users/login.html")


def register_view(request):
    return render(request, "users/register.html")


def profile_view(request):
    return render(request, "users/profile.html")


def imprint(request):
    return render(request, "users/imprint.html")


def privacy_policy(request):
    return render(request, "users/privacy_policy.html")


def terms_of_service(request):
    return render(request, "users/terms_of_service.html")


def cookie_policy(request):
    return render(request, "users/cookie_policy.html")

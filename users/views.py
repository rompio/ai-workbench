from django.http import HttpResponse


def login_view(request):
    return HttpResponse("This is the login page.")


def register_view(request):
    return HttpResponse("This is the registration page.")


def profile_view(request):
    return HttpResponse("This is the profile page.")

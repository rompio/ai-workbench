from django.urls import path
from . import views
from .views import register_view, login_view, logout_view

app_name = "users"


urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("imprint/", views.imprint, name="imprint"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path("cookie-policy/", views.cookie_policy, name="cookie_policy"),
]

from django.urls import include, path

from . import views


urlpatterns = [
    path("account/", views.dashboard, name="account_dashboard"),
    path("account/register/", views.register, name="account_register"),
    path("account/login/", views.LoginView.as_view(), name="account_login"),
    path("account/logout/", views.LogoutView.as_view(), name="account_logout"),
    path("account/signup/", views.SignupView.as_view(), name="account_signup"),
    path("account/settings/", views.SettingsView.as_view(), name="account_settings"),
    path("account/", include("account.urls")),
]

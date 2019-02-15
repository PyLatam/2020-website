from django.urls import include, path

from . import views


urlpatterns = [
    path("account/login/", views.LoginView.as_view(), name="account_login"),
    path("account/signup/", views.SignupView.as_view(), name="account_signup"),
    path('account/', include("account.urls")),
]

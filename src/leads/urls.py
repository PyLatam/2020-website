from django.urls import path

from . import views


urlpatterns = [
    path("register/<uuid:username>/", views.register_lead, name="register_lead"),
]

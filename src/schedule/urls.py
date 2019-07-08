from django.views.generic.detail import DetailView
from django.urls import path

from . import views


urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("<uuid:slug>/", DetailView.as_view(), name="talk_view"),
]

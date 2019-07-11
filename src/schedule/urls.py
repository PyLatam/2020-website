from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.landing, name="landing_page"),
    path("<slug:slug>/", views.TalkDetail.as_view(), name="talk_view"),
]

# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("external/", views.handle_external_request, name="external"),
    path("<str:client_id>/", views.room, name="room"),
]
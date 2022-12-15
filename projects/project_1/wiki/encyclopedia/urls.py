from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("add", views.add, name="add"),
    path("<str:entry>/edit", views.edit, name="edit")
]

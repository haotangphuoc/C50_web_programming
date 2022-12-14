from django.urls import path
from . import views

urlpatterns = [
    path('page', views.index, name="index"),
    path("<str:name>", views.greet, name="greet")
]
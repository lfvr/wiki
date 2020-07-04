from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="info"),
    path("search", views.page, name="search"),
    path("new", views.new, name="new"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/delete", views.delete, name="delete")
]
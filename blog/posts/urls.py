from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="posts.index"),
    path("create/", views.create, name="posts.create"),
]

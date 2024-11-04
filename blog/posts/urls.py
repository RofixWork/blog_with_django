from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="posts.home"),
    path("dashboard/", views.index, name="posts.index"),
    path("create/", views.create, name="posts.create"),
    path("<int:id>/", views.update, name="posts.update"),
]

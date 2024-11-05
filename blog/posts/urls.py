from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="posts.home"),
    path("dashboard/", views.index, name="posts.index"),
    path("profile/", views.profile, name="posts.profile"),
    path("create/", views.create, name="posts.create"),
    path("post/<int:id>/", views.show, name="posts.show"),
    path("<int:id>/", views.update, name="posts.update"),
    path("delete/<int:id>/", views.delete, name="posts.delete"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:query>", views.wiki, name="wiki"),
    path("create", views.create_page, name="create"),
    path("search", views.search, name="search")
]

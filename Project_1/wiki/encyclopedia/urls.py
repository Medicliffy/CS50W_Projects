from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_page, name="new_page"),
    path("wiki/<str:entry_name>", views.entry_page, name="entry"),
    path("search", views.search, name="search"),
    path("edit/<str:entry_name>", views.edit_entry, name="edit")
]

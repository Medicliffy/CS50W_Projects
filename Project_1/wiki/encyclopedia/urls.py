from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_page, name="new_page"),
    path("<str:entry_name>", views.entry_page, name="entry"),
]

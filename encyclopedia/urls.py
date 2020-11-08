from django.urls import path

from . import views
import re

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="title"),
    path("/random_page",views.random_page,name="random_page"),
    path("/new_page",views.new_page,name="new_page"),
    path("/edit_page",views.edit_page,name="edit_page"),


]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry,name="entry"),
    path("/wiki/results", views.results , name="results"),
    path("/wiki/newpage",views.newpage,name="newpage"),
    path("wiki/edit/<str:title>",views.edit,name="edit"),
]

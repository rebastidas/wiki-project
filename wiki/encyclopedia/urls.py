from django.urls import path

from . import views

app_name="wiki"
 
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.title, name="title"),
    path("matchs/", views.matchs, name="matchs"),
    path("newentry/",views.newentry, name="newentry"),
    path("newcreation/", views.newcreation, name="newcreation"),
    path("editentry/<title>", views.editentry, name="editentry"),
    path("edition/", views.edition, name="edition"),
    path("random/", views.random, name="random")
]

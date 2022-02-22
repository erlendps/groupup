from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name = "register"),
    path("login/", views.homepage, name = "index"),
    path("groups/<int:pk>/", views.group_site, name="group_site"),
    path("groups/<int:pk>/matches", views.group_matches, name="group_matches"),
]

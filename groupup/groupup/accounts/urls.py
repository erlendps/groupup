from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name = "register"),
    path("login/", views.index, name = "index"),
    path("", views.homepage, name="homepage"),
    path("groups/<int:pk>/", views.group_site, name="group_site"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("groups/<int:pk>/", views.group_site, name="group_site"),
]
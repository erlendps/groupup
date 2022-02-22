from django.urls import path
from . import views

urlpatterns = [
    path('create-group', views.handle_create_group)
]
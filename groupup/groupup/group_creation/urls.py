from django.urls import path
from . import views

urlpatterns = [
    path('create-group', views.UserGroupCreateView.as_view())
]
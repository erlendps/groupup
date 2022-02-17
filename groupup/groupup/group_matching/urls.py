from django.urls import path
from . import views

urlpatterns = [
    path('group/<int:pk>', views.group_browsing),
    path('sendmatchrequest/<int:pk>', views.send_match_request)
] 
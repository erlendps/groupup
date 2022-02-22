from django.urls import path
from . import views

urlpatterns = [
    path('group/<int:pk>', views.group_browsing),
    path('sendmatchrequest/<int:pk>', views.send_match_request),
    path('viewmatchrequests/<int:pk>', views.view_match_requests),
    path('handle_requests/<int:pk>', views.handle_match_request),
] 
from django.urls import path
from . import views

app_name = "group_admin"

urlpatterns = [
    path('', views.admin_index, name="admin_index"),
    path('groups/', views.all_groups, name='groups'),
    path('groups/<int:pk>', views.group_browsing, name='group_browsing'),
    path('sendmatchrequest/<int:pk>', views.send_match_request, name='send_match'),
    path('viewmatchrequests/<int:pk>', views.view_match_requests, name='view_match'),
    path('handle_requests/<int:pk>', views.handle_match_request, name='handle_request'),
    path('groups/<int:pk>/add_date', views.add_date, name='add_date'),
    path('groups/<int:pk>/remove_date', views.remove_date, name='remove_date')
] 
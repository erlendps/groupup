from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name = "register"),
    path("login/", views.homepage, name = "index"),
    path("groups/", views.all_groups, name="groups"),
    path("groups/<int:pk>/", views.group_site, name="group_site"),
    path("groups/<int:pk>/matches", views.group_matches, name="group_matches"),
    path("profile/invites", views.show_invites, name="invites"),
    path("profile/acceptinvite/<int:pk>", views.accept_invite, name="accept_invite"),
    path("profile/declineinvite/<int:pk>", views.decline_invite, name="decline_invite"),
]

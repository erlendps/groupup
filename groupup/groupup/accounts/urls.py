from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name = "register"),
    path("login/", views.homepage, name = "index"),
    path("groups/<int:pk>/", views.group_site, name="group_site"),
    path("groups/<int:pk>/matches", views.group_matches, name="group_matches"),
    path("profile/invites", views.show_invites, name="invites"),
    path("profile/acceptinvite/<int:pk>", views.accept_invite),
    path("profile/declineinvite/<int:pk>", views.decline_invite),
]

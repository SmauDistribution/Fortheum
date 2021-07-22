from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="Home"),
    path("discussion/<str:dis_t>", views.discussion, name="Discussion"),
    path("newmessage", views.newmessage_request, name="NewMessage"),
    path("login", views.login_request, name="Login"),
    path("logout", views.logout_request, name="Logout"),
    path("register", views.register, name="Register"),
    path("profile", views.profile, name="Profile"),
    path("newdiscussion", views.newdiscussion_request, name="NewDiscussion"),
    path("deletediscussion/<str:dis_t>", views.deletedis_request, name="DeleteDiscussion"),
    path("editdiscussion/<str:old_title>", views.editdiscussion_request, name="EditDiscussion"),
    path("editprofile", views.editprofile_request, name="EditProfile"),
    path("editcredentials", views.editcredentials_request, name="EditCredentials"),
    path("rules", views.rules_page, name="Rules"),
]

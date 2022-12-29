from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="Home"),
    path("login_page", views.login_page, name="Login_page"),
    path("register_page", views.register_page, name="Register_page"),
    path("Logout", views.logout_page, name="Logout_page"),
    path("profile_settings", views.profile_setting, name="Profile_settings"),
    path("upload_post", views.upload_post, name="Upload_post"),
    path("like_post", views.like_post, name="Like_post"),
    path("profile/<str:pk>", views.profile, name="Profile"),
    path("follow", views.follow, name="Follow"),
    path("search", views.search, name="Search"),
    path("inbox", views.inbox, name="Inbox"),
    path("view_msg/<str:pk>", views.view_msg, name="View_msg"),
    path("send_msg", views.send_msg, name="Send_msg")
]

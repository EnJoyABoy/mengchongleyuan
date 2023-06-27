from django.contrib import admin
from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path('register', views.RegisterView.as_view(), name='register'),
    re_path('usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/', views.UsernameCountView.as_view(), name='usernamecont'),
    re_path('login', views.LoginView.as_view(), name='login'),
    re_path('logout', views.LogoutView.as_view(), name='logout'),
    re_path('myblogs', views.MyblogsView.as_view(), name='myblogs'),
]

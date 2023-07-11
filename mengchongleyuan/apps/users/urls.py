from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^register', views.RegisterView.as_view(), name='register'),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/', views.UsernameCountView.as_view(), name='usernamecont'),
    re_path(r'^login', views.LoginView.as_view(), name='login'),
    re_path(r'^logout', views.LogoutView.as_view(), name='logout'),
    re_path(r'^myblogs', views.MyblogsView.as_view(), name='myblogs'),
    re_path(r'^getcountblog', views.GetcountblogsView.as_view(), name='getcountblog'),
    re_path(r'^usermobile/(?P<usermobile>[0-9]{11})/count/', views.UsermobileCountView.as_view(), name='usermobilecont'),
]

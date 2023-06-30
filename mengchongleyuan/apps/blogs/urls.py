from django.urls import re_path
from . import views


urlpatterns = [
    # 首页路由
    re_path(r'^create_blogs', views.CreateblogsView.as_view(), name='create_blogs'),
    re_path(r'^getblogs', views.GetblogsView.as_view(), name='get_blogs'),
    re_path(r'^getmyblogs', views.GetmyblogsView.as_view(), name='get_myblogs'),
]
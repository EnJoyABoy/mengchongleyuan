from django.urls import path, re_path
from . import views


urlpatterns = [
    # 首页路由
    re_path('create_blogs', views.CewateblogsView.as_view(), name='create_blogs'),
]
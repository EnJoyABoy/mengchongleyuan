from django.urls import path, re_path
from . import views


urlpatterns = [
    # 首页路由
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^index', views.IndexView.as_view()),
]
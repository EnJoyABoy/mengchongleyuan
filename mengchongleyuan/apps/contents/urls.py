from django.urls import path
from . import views


urlpatterns = [
    # 首页路由
    path('', views.IndexView.as_view(), name='index'),
]
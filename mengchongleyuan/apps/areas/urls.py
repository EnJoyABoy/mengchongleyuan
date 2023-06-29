from django.urls import re_path
from . import views


urlpatterns = [
    re_path('areas', views.AreasView.as_view(), name='areas'),
]
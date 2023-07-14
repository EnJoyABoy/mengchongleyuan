from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)', views.ImageCodeView.as_view(), name='image_codes'),
    re_path(r'^verification_img_code', views.VerificationImgCodeView.as_view(), name='verification_img_code'),
]
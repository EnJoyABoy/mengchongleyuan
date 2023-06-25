from django.contrib.auth.backends import ModelBackend
import re
from apps.users.models import User

def get_user_by_username(username):
    try:
        if re.match(r'1[3-9]\d{9}', username):
            # username 是手机号
            user = User.objects.get(mobile=username)

        else:
            # username 是用户名
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    return user


class UsernameMobileModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        # 1. 先查询用户
        # username 有可能是 手机号 也有可能是用户名
        # 通过对username进行正则来区分
        user = get_user_by_username(username)
        # 2. 判断用户的密码是否正确
        if user is not None and user.check_password(password):
            return user
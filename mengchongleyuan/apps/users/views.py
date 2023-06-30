from django.shortcuts import render, redirect, reverse
from django.views import View
from django import http
from apps.users.models import User
import re
import logging
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from apps.blogs.models import Blogs
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger('django')


# Create your views here.
# 注册视图
class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        # 数据的验证
        # 验证必传的数据是否有值 all([el,el,el]) el必须有值 只要有一个为None 则为False
        if not all([username, password, password2, mobile]):
            return http.HttpResponseBadRequest('参数有问题')
        # 判断用户名是否符合规则 判断 5-20位 数字 字母 _
        if not re.match(r'[0-9a-zA-Z_]{5,20}', username):
            return http.HttpResponseBadRequest('用户名不合法')
        # 判断密码是否符合规则
        if not re.match(r'[0-9a-zA-Z_]{8,20}', password):
            return http.HttpResponseBadRequest('密码不合法')
        # 判断确认密码和密码是否一致
        if password != password2:
            return http.HttpResponseBadRequest('密码不一致')
        # 判断手机号是否符合规则
        if not re.match(r'1[3-9]\d{9}', mobile):
            return http.HttpResponseBadRequest('手机号不符合规则')

        # 验证数据没有问题才入库
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseBadRequest('数据库异常')

        # 注册完成之后,默认认为用户已经登陆 保持登陆的状态
        # 系统也能自己去实现登陆状态的保持
        login(request, user)

        # 跳转到首页
        return redirect(reverse('contents:index'))


# 登入视图
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 后端需要接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 判断参数是否齐全
        if not all([username, password]):
            return http.HttpResponseBadRequest('缺少必须的参数')
        # 判断用户名是否符合规则
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseBadRequest('用户名不符合规则')
        # 判断密码是否符合规则
        if not re.match(r'', password):
            return http.HttpResponseBadRequest('密码不符合规则')
        # 验证用户名和密码：django的认证后端或自己查询数据库验证
        # 如果用户名和密码正确,则返回user，否则返回None
        user = authenticate(username=username, password=password)

        if user is not None:
            # 如果验证成功则登陆,状态保持
            login(request, user)
            # 如果有next参数,则跳转到指定页面
            # 如果没有next参数,则跳转到首页
            next = request.GET.get('next')
            if next:
                response = redirect(next)
            else:
                response = redirect(reverse('contents:index'))
            # 设置cookie
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
            return response
        else:
            # 登陆失败
            return render(request, 'login.html', context={'account_errmsg': '用户名或密码错误'})


# 在注册时Vue发起ajax请求验证数据库中是否有相同用户名
class UsernameCountView(View):

    def get(self, request, username):
        # 查询数据库,通过查询记录的count来判断是否重复 0表示没有重复 1表示重复
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '数据库异常'})
        # 返回相应
        return http.JsonResponse({'code': 0, 'count': count})


# 退出登入，用户点击退出,就把登陆的信息删除
class LogoutView(View):

    def get(self, request):
        # 系统其他也给我们提供了退出的方法
        logout(request)

        # 退出之后,我们要跳转到指定页面 还跳转到首页
        response = redirect(reverse('contents:index'))
        # 需要额外删除cookie中的name,因为我们首页的用户信息展示是通过username来判断
        response.delete_cookie('username')

        return response


class MyblogsView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'myblogs.html')


from django.shortcuts import render, redirect, reverse
from django.views import View
from django import http
from apps.users.models import User
import re
import logging


logger = logging.getLogger('django')
# Create your views here.
# 注册视图
class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = request.POST
        username = data.get('username')
        passwrod = data.get('password')
        passwrod2 = data.get('password2')
        mobile = data.get('mobile')
        # 数据的验证
        # 验证必传的数据是否有值 all([el,el,el]) el必须有值 只要有一个为None 则为False
        if not all([username, passwrod, passwrod2, mobile]):
            return http.HttpResponseBadRequest('参数有问题')
        # 判断用户名是否符合规则 判断 5-20位 数字 字母 _
        if not re.match(r'[0-9a-zA-Z_]{5,20}', username):
            return http.HttpResponseBadRequest('用户名不合法')
        # 判断密码是否符合规则
        if not re.match(r'[0-9a-zA-Z_]{8,20}', passwrod):
            return http.HttpResponseBadRequest('密码不合法')
        # 判断确认密码和密码是否一致
        if passwrod != passwrod2:
            return http.HttpResponseBadRequest('密码不一致')
        # 判断手机号是否符合规则
        if not re.match(r'1[3-9]\d{9}', mobile):
            return http.HttpResponseBadRequest('手机号不符合规则')

        # 验证数据没有问题才入库
        try:
            user = User.objects.create_user(username=username, password=passwrod, mobile=mobile)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseBadRequest('数据库异常')

        # 注册完成之后,默认认为用户已经登陆 保持登陆的状态
        # 系统也能自己去实现登陆状态的保持
        from django.contrib.auth import login
        login(request, user)

        # 跳转到首页
        return redirect(reverse('contents:index'))


# 登入视图
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

# 在注册时Vue发起ajax请求验证数据库中是否有相同用户名
class UsernameCountView(View):

    def get(self,request,username):
        # 查询数据库,通过查询记录的count来判断是否重复 0表示没有重复 1表示重复
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':400,'errmsg':'数据库异常'})
        # 返回相应
        return http.JsonResponse({'code':0,'count':count})

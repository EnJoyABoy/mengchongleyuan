from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from apps.blogs.models import Blogs
import logging
from apps.areas.models import Area
from apps.users.models import User
import json
from utils.response_code import RETCODE


logger = logging.getLogger('django')


class CreateblogsView(LoginRequiredMixin, View):

    # 创建博客需求
    def get(self, request):
        return render(request, 'create_blogs.html')

    def post(self, request):
        # 接收数据
        data = request.POST
        contents = data.get('blogs')
        times = data.get('blogs_time')
        province = data.get('province')
        city = data.get('city')
        district = data.get('district')
        address = data.get('blogs_address')

        # 验证数据
        if not all([contents, times, province, city, district, address]):
            return http.HttpResponseBadRequest('缺少必传参数')

        province = Area.objects.filter(id=province)
        city = Area.objects.filter(id=city)
        district = Area.objects.filter(id=district)

        # 数据入库
        try:
            blogs = Blogs.objects.create(
                user=request.user,
                province=province[0],
                city=city[0],
                district=district[0],
                address=address,
                contents=contents,
                times=times
            )
        except Exception as e:
            logger.error(e)
            return http.HttpResponseBadRequest('数据库异常')

        # 跳转到首页
        return redirect(reverse('contents:index'))


# Vue发起aja请求到这读取数据库内容并返回至vue中渲染前端页面（首页）
class GetblogsView(View):

    def get(self, request):
        # 获取博客信息
        blogs = Blogs.objects.filter()
        blog_list = []
        for blog in blogs:
            blog_list.append({
                'contents': blog.contents,
                'times': blog.times,
                'province': str(blog.province),
                'city': str(blog.city),
                'district': str(blog.district),
                'address': blog.address,
                'user': str(blog.user),
                'mobile': User.objects.filter(username=blog.user)[0].mobile
            })
        context = {
            'blogs': blog_list
        }
        # 返回数据至Vue中
        return http.JsonResponse(context)

class GetmyblogsView(LoginRequiredMixin, View):

    def get(self, request):
        # 获取用户信息
        user = request.user
        # 如果是登入状态
        blog_list = []
        if user.is_authenticated:
            blogs = Blogs.objects.filter(user=user)
            for blog in blogs:
                blog_list.append({
                    'id': blog.id,
                    'contents': blog.contents,
                    'times': blog.times,
                    'province': str(blog.province),
                    'city': str(blog.city),
                    'district': str(blog.district),
                    'address': blog.address,
                    'user': str(blog.user),
                    'mobile': User.objects.filter(username=blog.user)[0].mobile
                })
        context = {
            'blogs': blog_list
        }
        # 返回数据至Vue中
        return http.JsonResponse(context)


# 实现内容删除
class DelmyblogsView(LoginRequiredMixin, View):

    def delete(self, request):
        # 获取数据
        data = json.loads(request.body.decode())
        blog_user = data.get('blog_user')
        blog_id = data.get('blog_id')

        if request.user.is_authenticated and str(request.user) == str(blog_user):
            # 查询数据库
            try:
                blog = Blogs.objects.get(id=blog_id)
            except Blogs.DoesNotExist:
                return http.JsonResponse({'code': RETCODE.NODATAERR, 'errmsg': '暂无此数据'})
            # 删除
            try:
                blog.delete()
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除失败'})

            # 返回响应
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
        else:
            return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': 'fail'})


from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from apps.blogs.models import Blogs
import logging
from apps.areas.models import Area


logger = logging.getLogger('django')
class CewateblogsView(LoginRequiredMixin, View):

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




from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from apps.blogs.models import Blogs


class IndexView(View):

    # 主页面展示
    def get(self, request):
        blogs = Blogs.objects.filter()
        blog_list = []
        for blog in blogs:
            blog_list.append({
                'contents': blog.contents,
                'times': blog.times,
                'province': blog.province,
                'city': blog.city,
                'district': blog.district,
                'address': blog.address,
                'user': blog.user
            })
        context = {
            'blogs': blog_list
        }
        return render(request, 'index.html', context=context)

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View

class CewateblogsView(View):

    # 创建博客需求
    def get(self, request):
        return render(request, 'create_blogs.html')

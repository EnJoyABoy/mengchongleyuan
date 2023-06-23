from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View


class IndexView(View):

    # 主页面展示
    def get(self, request):
        return render(request, 'index.html')

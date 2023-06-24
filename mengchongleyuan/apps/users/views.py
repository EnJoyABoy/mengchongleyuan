from django.shortcuts import render, redirect, reverse
from django.views import View


# Create your views here.
# 注册视图
class RegisterView(View):

    def get(self, request):
        # path = reverse('users:register')
        # return redirect(path)
        return render(request, 'register.html')

# 登入视图
class LoginView(View):

    def get(self, request):
        # path = reverse('users:login')
        # return redirect(path)

        return render(request, 'login.html')

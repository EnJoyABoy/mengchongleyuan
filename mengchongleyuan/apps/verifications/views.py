from django import http
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from utils.response_code import RETCODE
import logging
logger = logging.getLogger('django')


# 获取图片验证码
class ImageCodeView(View):

    def get(self, request, uuid):
        # 1.生成图片验证码和获取图片验证码的内容
        text, image = captcha.generate_captcha()
        # 2.1连接redis
        redis_conn = get_redis_connection('code')
        # 2.2将 图片验证码保存起来 uuid:xxxx 有有效期
        redis_conn.setex('img_%s'%uuid, 300, text)
        # 3.返回图片验证码  告知浏览器 这是个图片
        return http.HttpResponse(image, content_type='image/jpeg')


# 图片验证码验证
class VerificationImgCodeView(View):
    def get(self, request):
        # 接收参数(图片验证码,uuid)
        img_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 获取redis中的验证码
        try:
            redis_conn = get_redis_connection('code')
            redis_code = redis_conn.get('img_%s' % uuid)
            if redis_code is None:
                return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码过期'})
            # 添加一个删除图片验证码的逻辑
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'redis有异常'})
        # 判断验证码是否正确
        if redis_code.decode().lower() != img_code.lower():
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '短信验证码错误'})
        # 验证成功
        else:
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})

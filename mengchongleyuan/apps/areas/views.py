from django.shortcuts import render
from django import http
from django.views import View
from apps.areas.models import Area
from utils.response_code import RETCODE
from django.core.cache import cache


# Create your views here.
class AreasView(View):

    def get(self, request):
        parent_id = request.GET.get('area_id')
        if parent_id is None:
            # 先获取缓存
            province_list = cache.get('pro')
            # 如果为空则获取，有则直接读取使用
            if province_list is None:
                # 查询 省的信息
                proviences = Area.objects.filter(parent_id=None)
                # [Area,Area,Area]
                province_list = []
                for item in proviences:
                    province_list.append({
                        'id': item.id,
                        'name': item.name
                    })
                # 将数据保存到缓存中
                cache.set('pro', province_list, 24*3600)
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'province_list': province_list})

        else:
            # 读取缓存
            sub_list = cache.get('sub_%s'%parent_id)
            if sub_list is None:
                # 查询市、地区信息
                sub_areas = Area.objects.filter(parent_id=parent_id)
                # [Area,Area,Area]
                sub_list = []
                for sub in sub_areas:
                    sub_list.append({
                        'id': sub.id,
                        'name': sub.name
                    })
                # 保存缓存
                cache.set('sub_%s'%parent_id, sub_list, 24*3600)

            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'sub_data': sub_list})

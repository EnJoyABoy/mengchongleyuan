from django.shortcuts import render

# Create your views here.
from django import http
from django.views import View
from apps.areas.models import Area
from utils.response_code import RETCODE


class AreasView(View):

    def get(self,request):
        parent_id = request.GET.get('area_id')
        if parent_id is None:
            # 查询 省的信息
            proviences = Area.objects.filter(parent_id=None)
            # [Area,Area,Area]

            provience_list = []
            for item in proviences:
                provience_list.append({
                    'id': item.id,
                    'name': item.name
                })
            return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'ok', 'province_list':provience_list})

        else:
            # 查询市、地区信息
            sub_areas = Area.objects.filter(parent_id=parent_id)
            # [Area,Area,Area]

            sub_list = []
            for sub in sub_areas:
                sub_list.append({
                    'id': sub.id,
                    'name': sub.name
                })

            return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'ok', 'sub_data':sub_list})

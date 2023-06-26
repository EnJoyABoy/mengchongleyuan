from django.db import models

# Create your models here.


class Blogs(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='blogs', verbose_name='用户')
    province = models.ForeignKey('areas.Area', on_delete=models.CASCADE, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.CASCADE, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.CASCADE, related_name='district_addresses', verbose_name='区')
    address = models.CharField(max_length=200, verbose_name='详细地址')
    contents = models.CharField(max_length=200, verbose_name='需求')
    times = models.CharField(max_length=200, verbose_name='时间')

    class Meta:
        db_table = 'tb_blogs'
        verbose_name = '需求博客'
        verbose_name_plural = verbose_name


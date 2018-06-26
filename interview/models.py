#  *_ coding=utf-8 _*_

# 所有charfield都需要加max_length

from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name="姓名", max_length=50)
    email = models.CharField(verbose_name="邮箱", max_length=50)
    password = models.CharField(verbose_name="密码", max_length=128)
    mobile = models.CharField(verbose_name="手机号码", max_length=11, blank=True, null=True)  # blank为可以空白(后台),null可以可以为空(数据库)
    birthday = models.DateField(verbose_name="生日", blank=True, null=True)
    gen = (
        ("male", "男"),
        ("female", "女")
    )
    gender = models.CharField(verbose_name="性别", choices=gen, default="male", max_length=10)
    image = models.ImageField(verbose_name="头像", upload_to="user/%Y/%m", blank=True, null=True)

    class Meta:  # 表述类,用于后台
        verbose_name = "用户"
        verbose_name_plural = verbose_name  # 复数与单数关联

    def __unicode__(self):
        return self.username




class Author(models.Model):

    # 作者表

    name = models.CharField(verbose_name="姓名", max_length=50)
    desc = models.TextField(verbose_name="简介", max_length=300)
    profession = models.CharField(verbose_name="专业", max_length= 50)
    years = (
        ("1", "2018届"),
        ("2", "2017届"),
        ("3", "2016届"),
        ("4", "2015届"),
    )
    year = models.CharField(verbose_name="年级", choices=years, default="1", max_length=10)

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Interview(models.Model):

    # 面试经验

    title = models.CharField(verbose_name="标题", max_length=50)
    desc = models.CharField(verbose_name="描述", max_length=100)
    # content = models.TextField(verbose_name="内容", max_length=5000)
    content = UEditorField(verbose_name="内容", width=700, height=200, default="",
                           imagePath="content/%(basename)s_%(datetime)s.%(extname)s",
                           filePath="content/%(basename)s_%(datetime)s.%(extname)s")

    image = models.ImageField(verbose_name="封面", upload_to="interview/%Y/%m")
    author = models.ForeignKey(Author, verbose_name="所属作者")
    company = models.CharField(verbose_name="公司", max_length=50)
    trades=(
        ("t1", "互联网"),
        ("t2", "网络安全"),
        ("t3", "运营商"),
        ("t4", "银行"),
        ("t5", "集成商"),
        ("t6", "国企"),
        ("t7", "云计算"),
        ("t8", "其他"),
    )
    trade = models.CharField(verbose_name="行业", choices=trades, default="t1", max_length=10)
    locations = (
        ("l1", "上海"),
        ("l2", "北京"),
        ("l3", "广州"),
        ("l4", "深圳"),
        ("l5", "全国"),
        ("l6", "其他"),
    )
    location = models.CharField(verbose_name="地区", choices=locations, default="l1", max_length=10)
    pub_time = models.DateTimeField(verbose_name="发布时间", default=datetime.now)  # datetimefield可以具体到分钟和时间,datefield只能具体到年月日,defualt=datetime需要导入datetime模块
    read_count = models.IntegerField(verbose_name="阅读次数", default=0)  # 可以根据阅读次数来排序热度

    class Meta:
        verbose_name = "面试经验"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title






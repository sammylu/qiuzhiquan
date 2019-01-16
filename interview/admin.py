# *__coding=utf-8__*

from django.contrib import admin
from models import User, Author, Interview  # 1.导入models模型类
# Register your models here.

# 2.集成admin.ModelAdmin,创建后台管理类


class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'email',)  # 显示
    list_filter = ('username', 'email',)  # 过滤器
    search_fields = ('username', 'email',)  # 搜索


class AuthorAdmin(admin.ModelAdmin):

    list_display = ('name', 'desc',)
    list_filter = ('name', 'desc',)
    search_fields = ('name', 'desc',)


class InterviewAdmin(admin.ModelAdmin):

    list_display = ('title', 'desc', 'company',)
    list_filter = ('title', 'desc', 'company',)
    search_fields = ('title', 'desc', 'company',)



#3.注册后台管理类

admin.site.register(User, UserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Interview, InterviewAdmin)
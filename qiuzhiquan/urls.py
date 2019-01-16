# _*_coding:utf-8 _*_

"""qiuzhiquan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.views.static import serve  # 文件图片解析模块
from settings import MEDIA_ROOT  # 模板文件图片解析路径

from interview.views import InterListview, InterDetailView, RegView, LoginView  # 导入View函数/类

from interview.views import InterListview, InterDetailView  # 导入View函数/类


urlpatterns = [
    url(r'^admin/', admin.site.urls),  # 后台admin的url映射
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),  # 管理媒体文件路径映射和处理模块
    url(r'^interlist/$', InterListview.as_view(), name="interlist"),  # 名企面经的url映射,name为别名映射
    url(r'^interdetail/(?P<interview_id>\d+)/$', InterDetailView.as_view(), name="interdetail"),  # 面经详情映射

    url(r'^ueditor/', include('DjangoUeditor.urls')),  # 副文本映射
    url(r'register/$', RegView.as_view(), name="register"),  # 用户注册映射
    url(r'login/$', LoginView.as_view(), name="login"),  # 用户登录映射

    url(r'^ueditor/', include('DjangoUeditor.urls')),  # 增加url映射

]

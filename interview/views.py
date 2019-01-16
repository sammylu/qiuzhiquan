# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View   # 导入view的基类
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 导入分页库的类

from django.db.models import Q  # 导入Q或逻辑模块搜索
from django.contrib.auth.hashers import make_password  # 导入密码加密模块
from django.contrib.auth import logout, login, authenticate  # 导入表单验证莫快
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from forms import RegForm, LoginForm  # 导入用户注册和登录模块
from models import Interview, Author, User
from models import Interview, Author  # 导入模板interwiew类
from django.db.models import Q  # 导入Q或逻辑模块搜索
# Create your views here.


class InterListview(View):
    """
    名企面经列表类
    """
    # 取出所有面经

    def get(self, request):
        all_interviews = Interview.objects.all()  # 获取所有INTERVIEW对象

    def get(self, request):
        all_interviews = Interview.objects.all()  # 获取所有INTERVIEW对象

    # 搜索模块
        keywords = request.GET.get('keywords', "")  # 获取keywords信息,没有设为空
        if keywords:
            all_interviews = all_interviews.filter(Q(title__icontains=keywords) | Q(desc__icontains=keywords) |
                                                   Q(content__icontains=keywords))
    # 基于公司的分类

        company = request.GET.get('company', "")  # 获取关键词,若没有设置为空
        if company:
            all_interviews = Interview.objects.filter(company=company)  # 获取公司面经标签

    # 基于行业的分类
        trade = request.GET.get('trade', "")  # 获取关键词,若没有设置为空
        if trade:
            all_interviews = Interview.objects.filter(trade=trade)

    # 基于年级的分类(通过年级找作者，通过作者找面经)
        year = request.GET.get('year', "")
        if year:
            authors = Author.objects.filter(year=year)  # 取出年级对应的作者
            all_interviews = Interview.objects.none()  # 设置空面经queryset
            for author in authors:  # 遍历作者
                interviews = author.interview_set.all()  # 获取每个作者对应的面经(author和interview存在一对多的外键关系,可以调用interview_set方法)
                all_interviews = all_interviews | interviews  # 将每个作者的面经合并起来(queryset)

    # 对面经页面列表进行分页处理
        try:
            page = request.GET.get('page', 1)  # 获取page参数,若没有的话则设置为1

        except(PageNotAnInteger, EmptyPage):  # 若出现异常,也设置为1
            page = 1
        p = Paginator(all_interviews, 4, request=request)  # 创建Paginator实例,创建Paginator实例,将面经request传递进来,设置每个页面项目数为2
        interviews = p.page(page)



        return render(request, "interview_list.html", {
            "all_interviews": interviews,  # 传递模板变量给模板文件
        })


class InterDetailView(View):
    """
    面经详情
    """
    def get(self, request, interview_id):  # 传入interview_id参数
        interview = Interview.objects.get(id=int(interview_id))  # 获取面经id

        # 增加文章的点击次数

        interview.read_count += 1
        interview.save()

        # 相关推荐(同公司)

        recommended_tag = interview.company  # 以公司作为推荐标签
        recommended_interviews = Interview.objects.filter(company=recommended_tag).exclude(id=int(interview_id)).order_by('-read_count')[:3]  # 基于id来排除

        # 更多推荐(同行业)

        recommended_tag2 = interview.trade  # 以行业作为推荐标签
        recommended_interviews2 = Interview.objects.filter(trade=recommended_tag2).exclude(company=recommended_tag).order_by('-read_count')[:3]  # 基于公司来排除
        return render(request, "interview_detail.html", {
            "interview": interview,  # 传递模板变量给interview 给模板文件interview_detail
            "recommended_interviews": recommended_interviews,
            "recommended_interviews2": recommended_interviews2,
        })


class RegView(View):
    """
    用户注册
    """
    def get(self, request):
        return render(request, "reg.html", {})

    def post(self, request):
        regform =RegForm(request.POST)  # 通过注册表单获取用户的POST信息
        if regform.is_valid():  # 若表单认证成功
            # 获取用户信息
            # username = request.POST.get("username", "")
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user = User()  # user模板实例
            # user.username = username
            user.email = email
            user.password = password
            user.password= make_password(password)
            user.save()  # 保存数据库
            return render(request, "login.html")  # 验证有效之后,返回登录页面
        else:
            return render(request, "reg.html", {"regform": regform})  # 验证失败,停留在注册页面


class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        return render(request, "login.html", {})
    def post(self,request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():  # 表单有效性验证成功
            username = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)  # 获取帐号验证
            if user is not None:
                login(request, user)  # 则登录帐号
            else:
                return render(request, 'login.html', {"error": '登录验证失败'})  #若帐号认证失败，返回登录页面
            return HttpResponseRedirect(reverse("index"))  # 重定向到首页
        else:
            return render(request, 'login.html', {"error": '登录验证失败'})



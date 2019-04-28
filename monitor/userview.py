from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import auth
from .userform import LoginForm
from .infogetter import InfoGetter


def login_redirect(request):
    return redirect('/login')


# 登录页
def login_page(request):
    return render(request, 'login.html')


# login逻辑判断
def user_login(request):
    login_form = LoginForm(request.POST)
    # 验证实例是否有效
    if login_form.is_valid():
        cd = login_form.cleaned_data
        # 验证用户是否存在，且用户名密码是否正确
        user = authenticate(username=cd['username'], password=cd['password'])
        # 如果用户通过认证
        if user:
            # 进行用户登录，且返回成功信息
            login(request, user)
            request.session['user'] = user.username
            # return HttpResponse("you are authenticated,welcome {}".format(user.username))
            context = {
                'data': user,
            }
            return redirect('/index', context)
        else:
            return HttpResponse("wrong username or password, authentication failed")
    # 实例无效
    else:
        return HttpResponse("Invalid login")


def index(request):
    # 还要做下身份验证判断，若没有进行验证要跳转到登录页面
    if not request.session['user']:
        return redirect('/login')

    context = dict(
        hosts_num=InfoGetter().index_top_info(),
    )
    return render(request, 'index.html', context)


def user_logout(request):
    if not request.session['user']:
        return redirect('/login')
    del request.session['user']
    return redirect('/login')

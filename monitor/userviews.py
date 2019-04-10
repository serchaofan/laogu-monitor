from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# django自带的用户认证方法authenticate和用户管理方法login
from .userform import LoginForm
from PIL import Image, ImageDraw, ImageFont
import random

# login页面
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
      return redirect('/dashboard', context)
    else:
      return HttpResponse("wrong username or password, authentication failed")
  # 实例无效
  else:
    return HttpResponse("Invalid login")


# def verifycode(request):
#   # bgColor背景色，设置偏暗
#   bgColor = (random.randrange(20, 100), random.randrange(20, 100), 0)
#   # 设置宽高
#   width = 95
#   height = 35
#   # 创建画布
#   image = Image.new('RGB', (width, height), bgColor)
#   # 创建字体对象
#   font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf", 30)
#   # 创建画笔
#   draw = ImageDraw.Draw(image)
#   # 创建文本内容
#   text = 'qwertyuQWERTYUIDFGHJKXCVBNMioasd12345678fghjklzxcvbnm'
#   text1 = ""
#   for i in range(4):
#     text1 = text1 + (text[random.randrange(0, len(text))])
#   # 通过session记录该字符串
#   request.session['verifycode'] = text1
#   # 绘制字符串
#   draw.text((0, 0), text1, (255, 255, 255), font=font)
#   # 保存在内存流中
#   from io import StringIO, BytesIO
#   buf = BytesIO()
#   image.save(buf, 'png')
#   # 将内存流的内容输出到客户端
#   return HttpResponse(buf.getvalue(), 'image/png')


def dashboard(request):
  return render(request, 'backends/dashboard.html')

def user_logout(request):
  del request.session['user']
  return redirect('/login')

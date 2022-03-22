import re
import time

from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from modelofshares import models

# {#author: Wangzehang Liyuanchi Huanyunbo#}
# {#date: 2022-03-19 ~ 2022-03-21#}
# {#info: regist html #}

# Create your views here.
from modelofshares.models import UserInfo, GPData, SessionData
from static.getdata.JS_Data_Get import parse_url, get_date, download, pd_sort, out


def login(request):
    if request.method == "POST":
        account = request.POST.get("account")
        print(1)
        password = request.POST.get("passwd")
        if connert(account, 1):
            user = UserInfo.objects.get(account=account)
            pwd = user.password
            if check_password(password, pwd):
                if user.is_active:
                    auth.login(request, user)
                    return redirect("/index")
                else:
                    messages.error(request, "账号没有激活")
                    return redirect("/login")
            else:
                messages.error(request, "账号/密码错误")
                return redirect("/login")
        else:
            messages.error(request, "账号不存在")
            return redirect("/login")

    return render(request, 'html/login.html')


@login_required(redirect_field_name="next", login_url="/login")
def index(request):
    print(request.user)
    datas = connert(None, 7)
    datas2 = connert(None, 8)
    list1 = []
    list_year = []
    list_y = []
    list_y_pre = []
    for data in datas:
        list1.append([data.date, data.open, data.close, data.lowest, data.highest])

    for i in datas2:
        list_year.append(i.year)
        list_y.append(i.y)
        list_y_pre.append(i.y_pre)
    if request.method == 'POST':
        gp = request.POST.get("gp")
        print(gp)
        try:
            y_pre = out(gp)
            print(y_pre[0])
            str1 = "预测明日收盘价："+str(y_pre[0])
            messages.add_message(request, messages.INFO,  str1)
            return redirect("/index")
        except:
            messages.add_message(request, messages.ERROR, "输入错误！")
            return redirect("/index", {"msg": "error"})

    request.session.set_expiry(0)
    return render(request, 'html/index.html',
                  {"list1": list1, "user": request.user, "year": list_year, "y": list_y, "y_pre": list_y_pre})


def regist(request):
    if request.method == "POST":
        data = {}
        flag = 0
        account = request.POST.get('account')
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        check_passwd = request.POST.get('checkpasswd')

        if checkpasswd(passwd, check_passwd) is False:
            data["password"] = "error"
            flag += 1

        if connert(username, 4) is True:
            data["username"] = "error"
            flag += 1

        print(flag)
        if flag == 0:
            data["account"] = account
            data["username"] = username
            data["password"] = passwd
            print("开始写入数据库中")
            connert(data, 2)
            messages.success(request, '注册成功，正在返回登录页面')
            return redirect('/login')
        messages.error(request, '注册失败')
        return redirect('/login')
    return render(request, 'html/regist.html')


def recompose(request):
    if request.method == "POST":
        data = {}
        flag = 0
        username = request.POST.get("username")
        password = request.POST.get("passwd")
        check_passwd = request.POST.get("checkpasswd")

        if connert(username, 4) is False:
            flag += 1

        if checkpasswd(password, check_passwd) is False:
            flag += 1

        if flag == 0:
            data["username"] = username
            data["password"] = password
            connert(data, 6)
            messages.success(request, "修改成功")
            return redirect('/login')

        messages.add_message(request, messages.INFO, '修改失败')
        return redirect('/login')
    return render(request, "html/recompose.html")


def checkpasswd(password, check_password):
    if password != check_password:
        return False
    elif len(password) < 8:
        return False
    else:
        print("密码正确")
        return True


def connert(data, item):
    try:

        if item == 1:
            res1 = UserInfo.objects.filter(account=data).exists()
            print(res1)
            return res1
        if item == 2:
            res2 = UserInfo.objects.create_user(**data)
            res2.save()
            print(res2)
            return True

        if item == 3:
            res3 = UserInfo.objects.filter(account=data["account"]).values("password").get()
            if data["password"] == res3["password"]:
                return True
            else:
                return False

        if item == 4:
            res4 = UserInfo.objects.filter(username=data).exists()
            print(res4)
            return res4

        if item == 5:
            res5 = UserInfo.objects.filter(password=data).exists()
            print(res5)
            return res5

        if item == 6:
            res6 = UserInfo.objects.get(username=data["username"])
            res6.set_password(data['password'])
            print(res6)
            return res6

        if item == 7:
            res7 = GPData.objects.all()
            print(res7)
            return res7

        if item == 8:
            res8 = SessionData.objects.all()
            print(res8)
            return res8

    except Exception:
        return False

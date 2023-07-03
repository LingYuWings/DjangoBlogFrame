from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

def index(req):
    return render(req,'index.html')

def login(request):
    error_msg=''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # use login function to log the user
            dj_login(request, user)
            # login success, return to main page
            return HttpResponseRedirect('/')
            
        else:
            # return login failed message
            error_msg='Wrong username or password'
    return render(request,'login.html',{'error_msg':error_msg})

def signout(req):
    logout(req)
    return HttpResponseRedirect("/")

def signUp(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
    
    return render(req,'signup.html')
        
        
    
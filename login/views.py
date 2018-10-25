import hashlib
from login import forms, models
from django.shortcuts import render, redirect


# Create your views here.models
def hash_code(s, salt='mysite_2'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Users.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = '密码不正确'
            except:
                message = '用户不存在'
        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(requset):
    if requset.session.get('is_login', None):
        return redirect('/index/')
    if requset.method == 'POST':
        register_form = forms.RegisterForm(requset.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不一致'
                return render(requset, 'login/register.html', locals())
            else:
                same_user_name = models.Users.objects.filter(name=username)
                if same_user_name:
                    message = "用户名已存在"
                    return render(request, 'login/register.html', locals())
                same_user_email = models.Users.objects.filter(email=email)
                if same_user_email:
                    message = "邮箱已被注册,请输入其它邮箱"
                    return render(request, 'login/register.html', locals())

                user = models.Users()
                user.name = username
                user.password = hash_code(password1)
                user.email = email
                user.sex = sex
                user.save()

                return redirect('/login/')

    register_form = forms.RegisterForm()
    return render(requset, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')



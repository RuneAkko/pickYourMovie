from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import UserProfile, UserAndMovie
from django.contrib.auth.models import User
from account.forms import LoginForm, RegisterForm, UserProfileForm

# Create your views here.
def account_login(req):
    if req.method == 'POST':
        login_form = LoginForm(req.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                username=cd['userName'],
                password=cd['passWord']
            )

            if user:
                login(req, user)
                return redirect('/')
            else:
                return HttpResponse("用户或密码错误！")
        else:
            return HttpResponse("格式错误")
    if req.method == 'GET':
        # login_form = LoginForm()
        # return render(req, 'login2.html', {'info': login_form})
        return render(req, 'login.html')

def register(req):
    if req.method == 'POST':
        user_form = RegisterForm(req.POST)
        # userprofile_form = UserProfileForm(req.POST)
        # print(user_form)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            # new_profile = userprofile_form.save(commit=False)
            # new_profile.user = new_user
            # new_profile.save()
            UserProfile.objects.create(
                user=new_user,
                dislike_sth="empty",
                like_sth="empty"
            )
            return redirect('/')
        else:
            return HttpResponse("can not register")
    else:
        user_form = RegisterForm()
        return render(req, "register.html", {'info': user_form})

@login_required
def logout(req):
    auth.logout(req)
    return redirect('/')

@login_required(login_url='/login')
def user_profile_display(req):
    user = User.objects.get(username=req.user.username)
    userprofile = UserProfile.objects.get(user=user)
    return render(req, 'test.html', {
        'user': user,
        'userprofile': userprofile
    })

@csrf_exempt
@require_POST
@login_required(login_url='/login')

def user_profile_edit(req):
    move_id = req.POST.get('id')
    action = req.POST.get('action')
    username = req.user.id
    if move_id and username:
        # try:
        temp = UserAndMovie(user_id=str(username), movie_id=str(move_id))
        temp.save()
        return HttpResponse("成功存储！")
        # except:

    return HttpResponse("1")





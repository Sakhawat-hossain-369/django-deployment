from django.shortcuts import render
from login_app.forms import UserForm , UserInfoForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from login_app.models import UserInfo

# Create your views here.
def base(request):
    diction={'title':'base page','text':'Hi this is base.html page'}
    return render(request,'login_app/base.html',context=diction)

def index(request):
    # Initialize the variables to None
    user_basic_info = None
    user_more_info = None
    
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        
        try:
            user_more_info = UserInfo.objects.get(user__pk=user_id)
        except UserInfo.DoesNotExist:
            user_more_info = None

    diction = {
        'user_basic_info': user_basic_info,
        'user_more_info': user_more_info
    }

    return render(request, 'login_app/index.html', context=diction)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user=user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            
            user_info.save()
            registered=True


    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    diction={'user_form':user_form, 'user_info_form':user_info_form,'registered':registered}
    return render(request,'login_app/register.html',context=diction)

def login_page(request):
    diction={}
    return render(request,'login_app/login.html',context=diction)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('login_app:index'))
            else:
                return HttpResponse("Accounts is not Active!")
        else:
            return HttpResponse("Login details are wrong!!")
        
    else:
        return render(request,'login_app/login.html',context={})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:index'))
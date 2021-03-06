from django.shortcuts import render, redirect, HttpResponse
from .forms import UserForm, LoginForm
from .models import AppUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from urllib import request
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from Screens.models import Screens
from Advertiser.models import AdMedia, DisplaysAd
import uuid
import json
from django.core.mail import send_mail
from Adware.settings import EMAIL_HOST_USER

def index(request):
    info = ""
    msgtype = ""
    user = request.user   # initialize user values
    roles = []
    roleURL = {}
    roleURL['vendor'] = '/scr'
    roleURL['advertiser'] = '/adv'
    obj = User()
    if request.method == 'POST':
        if 'signup' in request.POST:
            print("signup_triggered")
            form = UserForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                email = form.cleaned_data['email']
                type = form.cleaned_data['type']
                try:
                    UserExist = User.objects.get(username=email)
                except User.DoesNotExist:
                    UserExist = None
                if UserExist:
                    UserType = [i.type for i in AppUser.objects.filter(User=UserExist)]
                    if type in UserType:
                        info = "User Already Exist"
                        msgtype = "error"
                    else:
                        info = 'User with different role exist'
                        msgtype = "warning"
                        # Multiple roles will be continues
                else:
                    obj.username = email
                    print(form.cleaned_data)
                    obj.set_password(form.cleaned_data['password1'])
                    obj.save()
                    o1 = AppUser()
                    o1.type = type
                    o1.User = obj
                    o1.save()
                    info = "user created successfully"
                    msgtype = "success"
                    #send_mail('Adware Welcomes you', 'signup successfull', EMAIL_HOST_USER, [email], fail_silently=False)
            else:
                info = "Passwords don't match"
                msgtype='error'

        elif 'login' in request.POST:
            print("login_triggered")
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                print(loginform.cleaned_data)
                user = loginform.cleaned_data['username']
                pswd = loginform.cleaned_data['password']
                user = authenticate(username=user,password=pswd)
                email = str(user)
                if user is not None:
                    info = "logged in successfully"
                    msgtype = "success"
                    login(request,user)
                    print(user)
                    #send_mail('Welcome Back',info, EMAIL_HOST_USER, [email], fail_silently=False)
                else:
                    info = "invalid credentials"
                    msgtype = "warning"
    if user and user.is_authenticated:
        """
        Defining roles for logged in user
        """
        roles = [i.type.lower() for i in AppUser.objects.filter(User=user)]
        roles = [(i, roleURL[i]) for i in roles]
    else:
        user=''
    return render(request, "index.html",{'f1': UserForm, 'f2': LoginForm, 'info': info, 'msgtype': msgtype, 'user': str(user).split("@")[0], 'roles': roles})

@login_required
def profile(request):
    """
    :param request: request
    :return: Profile page
    Page to redirect to home page after successful login attempt
    """
    return redirect('/')


def signup(request, type):
    """
    :param request: request
    :return: Signup Form / Redirect to login
    """
    form = UserForm()

    if request.method == "POST":
        obj = User()
        form = UserForm(request.POST, instance=obj)
        if form.is_valid():
            obj.username = obj.email
            print(form.cleaned_data)
            obj.set_password(form.cleaned_data['password1'])
            try:
                obj.save()
                o1 = AppUser()
                o1.User = obj
                o1.type = type
                o1.save()
                print(AppUser.objects.all())
            except IntegrityError:
                print('triggered')
                # Invoked in case of redundant credentials
                return redirect('login')
            return redirect('login')
    return render(request, 'registration/signup.html', {'form': form})


def handler404(request,exception):
    return render(request, '404.html',status=404)


def handler403(request,exception):
    return render(request, '403.html', status=403)


def api(request):
    id=request.GET.get('id',None)
    response={'status':'ok', 'media_path':[]}
    try:
        id = uuid.UUID(id)
        screen = None
        for screens in Screens.objects.all():
            if screens.id == id:
                screen=screens
                break
        if not screen:
            response['status'] = 'not found'
        else:
            for obj in DisplaysAd.objects.all():
                if obj.screen == screen:
                    response['media_path'].append(obj.ad.media.name)

    except ValueError:
        print('ValueError')
        response['status'] = 'not found'
    return HttpResponse(json.dumps(response), content_type="application/json")

def privacy_policy(request):
    return render(request, 'Advertiser/privacy-policy.html')



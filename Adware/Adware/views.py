from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm
from .models import AppUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required


def index(request):
    info = ""
    if request.method == 'POST':
        obj = User()
        form = UserForm(request.POST)
        info = "some error occured"
        print(form.is_valid())

        if True:
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
                else:
                    info = 'User with different role exist'
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
    form = UserForm()
    loginForm = LoginForm()
    user=''
    if request.user.is_authenticated:
        user=request.user.username
    return render(request, "index.html", {'f1': form, 'f2': LoginForm, 'info': info,'user':user})


@login_required
def profile(request):
    """
    :param request: reqeest
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

from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


@login_required
def profile(request):
    """
    :param request: reqeest
    :return: Profile page
    Profile page
    """
    return render(request, 'registration/profile.html', {'username': request.user})


def signup(request):
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
            except IntegrityError:
                return redirect('login')
            return redirect('login')
    return render(request, 'registration/signup.html', {'form': form})

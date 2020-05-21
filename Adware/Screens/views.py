from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    form = ScreenForm()
    return render(request, "Screens/index.html", {'f1':form})


@login_required
def new_scr(request):
    if request.method == 'POST':
        obj = Screens()
        form = ScreenForm(request.POST, instance=obj)
        if form.is_valid():
            obj.owner = request.user
            obj.save()
            return redirect('/')
    form = ScreenForm()
    return render(request, "Screens/new.html", {'f1': form})

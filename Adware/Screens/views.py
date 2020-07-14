from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import requests


@login_required
def index(request):
    form = ScreenForm()
    screens = []
    msg = request.GET.get('info', '')
    msgtype = request.GET.get('msgtype', 'error')
    for screen in Screens.objects.all():
        if request.user == screen.owner:
            screens.append(screen)
    #print(uuids)
    print(msg)
    print(msgtype)
    return render(request, "Screens/index.html",
                  {'f1':form,
                   'user':str(request.user).split("@")[0],
                   'screens':screens,
                   'info':msg,
                   'msgtype':msgtype,
                   })


@login_required
def new_scr(request):
    if request.method == 'POST':
        obj = Screens()
        form = ScreenForm(request.POST, instance=obj)
        if form.is_valid():
            obj.owner = request.user
            obj.save()
            print(get_uuid(obj.auto_id))
            return redirect('/scr?info=New Screen added&msgtype=success')

    return redirect('/scr?info=Some Error Occurred&msgtype=error')


def display(request):
    uuid = request.GET.get('uuid','')
    if uuid:
        url='http://127.0.0.1:8000/api?id='+uuid
        print(url)
        data = requests.request('GET',url)
        data = data.json()
        if data['status'] == 'ok':
            urls = data['media_path']
            return render(request,'Screens/display.html',{'urls':urls})
    return render(request,'Screens/display_form.html')


def get_uuid(x):
    for i in Screens.objects.all():
        if i.auto_id == x:
            return i.id
    return None

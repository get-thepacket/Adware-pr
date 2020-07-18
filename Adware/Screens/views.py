from django.shortcuts import render, redirect
from django.http import HttpResponse
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


@login_required
def display(request):
    uuid = request.GET.get('uuid','')
    screen_empty = "not_empty";
    if uuid:
        url='http://127.0.0.1:8000/api?id='+uuid
        print(url)
        data = requests.request('GET',url)
        data = data.json()
        if data['status'] == 'ok':
            screen_name = Screens.objects.get(id=uuid)
            screen_name = screen_name.description
            print(screen_name)
            urls = data['media_path']
            if len(urls)==1:
                urls.append(urls[0])
            print(len(urls))
            if len(urls)==0:
                screen_empty = "";
            return render(request,'Screens/display.html',{'urls':urls , 'screen_empty':screen_empty,'screen_name': screen_name})
    return render(request,'Screens/display_form.html')


def get_uuid(x):
    for i in Screens.objects.all():
        if i.auto_id == x:
            return i.id
    return None


def calculate_cost(request):
    for screen in Screens.objects.all():
        try:
            obj = ScreenStats.objects.get(screen=screen)
        except ScreenStats.DoesNotExist:
            obj = ScreenStats(screen=screen, queue=bytes("",'utf-8'), sum=0)
            obj.save()
        queue = list(map(int,obj.queue.split()))
        sm = obj.sum

        if len(queue)>=10:
            sm-=queue.pop(0)
        print(queue)
        sm+=screen.ad_available
        queue.append(screen.ad_available)
        obj.queue = bytes(" ".join(map(str,queue)),'utf-8')
        obj.sum = sm
        obj.save()

    return HttpResponse('success')


def update_cost():
    for screen in Screens.objects.all():
        print(screen)



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import requests


base_cost = {'Big':100, 'Medium': 70, 'Small': 40}


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
            obj = ScreenStats(screen=screen, queue="", sum=0)
        queue = list(map(int,obj.queue.split()))
        sm = obj.sum

        if len(queue)>=10:
            sm-=queue.pop(0)
        print(queue)
        sm+=screen.ad_available
        queue.append(screen.ad_available)
        obj.queue =" ".join(map(str,queue))
        obj.sum = sm
        obj.save()
    update_cost()
    return HttpResponse('success')


def cost_function(key_value):
    # Add cost function implementation here
    # key value is avg no. of screens available over last 10 days.
    result = key_value
    return result


def update_cost():
    for screen in Screens.objects.all():
        try:

            obj1 = ScreenCost.objects.get(screen=screen)
        except ScreenCost.DoesNotExist:
            print('not')
            obj1 = ScreenCost(screen=screen, cost=0)
        try:
            print('not')
            obj2 = ScreenStats.objects.get(screen=screen)
        except ScreenStats.DoesNotExist:
            obj2 = ScreenStats(screen=screen, queue="", sum=0)
        ln = len(obj2.queue.split(" "))
        print(cost_function(obj2.sum / ln))
        obj1.cost = int(cost_function(obj2.sum/ln))
        obj1.save()


@login_required
def get_cost(request):
    id = request.GET.get('id','')
    if not id:
        return HttpResponse('0')
    try:
        screen_obj = Screens.objects.get(auto_id=id)
        screencost_obj = ScreenCost.objects.get(screen=screen_obj)
    except Screens.DoesNotExist:
        return HttpResponse('0')
    except ScreenCost.DoesNotExist:
        return HttpResponse('0')
    cost = base_cost[screen_obj.type]
    cost += screencost_obj.cost
    return HttpResponse(str(cost))


def get_cost_inner(id):
    try:
        screen_obj = Screens.objects.get(auto_id=id)
        screencost_obj = ScreenCost.objects.get(screen=screen_obj)
    except Screens.DoesNotExist:
        return HttpResponse('0')
    except ScreenCost.DoesNotExist:
        return HttpResponse('0')
    cost = base_cost[screen_obj.type]
    cost += screencost_obj.cost
    return cost






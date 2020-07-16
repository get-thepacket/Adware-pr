from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdMediaForm
from .models import AdMedia, DisplaysAd
from Screens.models import Screens, Waitlist, WaitCount
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

"""
Note: put login required decorator for all functions
"""

pricing = {'Big': 100, "Medium": 50, "Small": 30}


@login_required
def index(request):
    form = AdMediaForm()
    user_media = AdMedia.objects.filter(username=request.user)
    msg = request.GET.get('info', '')
    msgtype = request.GET.get('msgtype', 'error')
    print(msg)
    print(msgtype)
    subscription = []
    total_cost = 0
    for sub in DisplaysAd.objects.all():
        if sub.ad.username == request.user:
            cost = pricing[sub.screen.type]
            subscription.append((sub, cost))
            total_cost+=cost
    print(subscription,total_cost)
    return render(request, "Advertiser/index.html",
                  {'user': str(request.user).split("@")[0],
                   'f1': form,
                   'AdMedia': user_media,
                   'info': msg,
                   'msgtype': msgtype,
                   'total_cost':total_cost,
                   'subscription':subscription,
                   })


@login_required
def new_adv(request):
    """
    Function for uploading new AdMedia to server.
    """
    print(request.method)
    if request.method == 'POST':

        obj = AdMedia()

        form = AdMediaForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            obj.username = request.user

            obj.save()

            return redirect('/adv?info=Advertisement uploaded&msgtype=success')

    return redirect('/adv?info=Some Error Occurred&msgtype=error')


@login_required
def view_media(request):
    """
    Function to view all uploaded media to the server.
    """

    user_media = AdMedia.objects.filter(username=request.user)

    return render(request, "Advertiser/view_media.html", {'AdMedia': user_media})


def media(request, media_name):
    """
    Function to securely access media files
    Secure Access removed to spped up API integration

    files = [str(i.media) for i in AdMedia.objects.filter(username=request.user)]

    if media_name not in files:
        return HttpResponse('Unauthorised', status=401)

    """

    img = open(settings.BASE_DIR + '/media/' + media_name, 'rb')

    return HttpResponse(img.read(), content_type="image/jpeg")


@login_required
def screen_select(request, ad_id):
    """
    function implements screen selections portal
    ad_id from get request
    todo: user interactive page
    todo: geo-location based selection
    """
    msg = request.GET.get('info', '')
    msgtype = request.GET.get('msgtype', 'error')

    search = request.GET.get('search', '')
    Screen = [i for i in Screens.objects.all() if i.ad_available > 0]
    query_result = []
    screen_size_filter_flag = False
    big_size_flag = False
    med_size_flag = False
    sml_size_flag = False
    if request.GET.get('big','')=='on':
        screen_size_filter_flag = True
        big_size_flag = True
    if request.GET.get('med','')=='on':
        screen_size_filter_flag = True
        med_size_flag = True
    if request.GET.get('sml','') == 'on':
        screen_size_filter_flag = True
        sml_size_flag = True

    for screen in Screen:
        # print(screen.address,screen.landmarks,search)
        if (search in screen.address) or (search in screen.landmarks):
            if screen_size_filter_flag:
                size = screen.type
                if size == 'Big' and big_size_flag:
                    query_result.append(screen)
                elif size == 'Small' and sml_size_flag:
                    query_result.append(screen)
                elif size == 'Medium' and med_size_flag:
                    query_result.append(screen)
                else:
                    continue
            else:
                query_result.append(screen)
    print(query_result)
    total_screens = len(query_result)
    print(total_screens)

    return render(request, 'Advertiser/publish.html',
                  {'total_screens': total_screens,
                   'query_result': query_result,
                   'ad_id': ad_id,
                   'bflag': big_size_flag,
                   'mflag': med_size_flag,
                   'sflag': sml_size_flag,
                   'search': search,
                   'info':msg,
                   'msgtype':msgtype})


@login_required
def publish(request, ad_id, screen_id):
    ad = None

    screen = None

    for ads in AdMedia.objects.all():
        print(ads.id)
        if ads.id == int(ad_id):
            ad = ads
            break
    for screens in Screens.objects.all():
        if screens.auto_id == int(screen_id):
            screen = screens
            break
    print(1, screen)
    print(2, ad)
    if not screen or not ad or ad.username != request.user:
        # Screen or Ad not found.
        # Advertisement does not belong to the current user.
        # Or Screen is occupied fully.
        return redirect('/adv/publish/' + str(ad_id) + '?info=Some Error Occurred&msgtype=error')
    if screen.ad_available <=0:
        return redirect('/adv/publish/' + str(ad_id) + '?info=Screen not available&msgtype=warning')
    display = DisplaysAd()
    display.ad = ad
    display.screen = screen
    screen.ad_available = screen.ad_available - 1
    screen.save()
    display.save()
    return redirect('/adv/publish/' + str(ad_id) + '?info=Advertisement Published&msgtype=success')


@login_required
def expire(request):
    if request.user.is_superuser:
        expiration_time = 0    # days
        query = DisplaysAd.objects.all()
        for obj in query:
            age = timezone.now() - obj.date_created
            print(age,age.days)
            if age.days >= expiration_time:
                screen = obj.screen
                screen.ad_available = screen.ad_available + 1
                screen.save()
                obj.delete()
        return HttpResponse('expired subscriptions removed')
    return redirect('/')


@login_required
def notify(request,screen_id):
    user = request.user
    screen = Screens.objects.get(auto_id=screen_id)
    waitlist_obj = Waitlist()
    waitlist_obj.user_waiting = user
    waitlist_obj.screen = screen
    waitlist_obj.save()




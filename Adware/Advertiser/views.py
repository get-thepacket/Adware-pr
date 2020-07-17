from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdMediaForm
from .models import AdMedia, DisplaysAd
from Screens.models import Screens, Waitlist, WaitCount
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
from django.core.mail import send_mail
from Adware.settings import EMAIL_HOST_USER

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


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
    user_media_pair = []
    temp=[]
    for i in user_media:
        if temp:
            temp.append(i)
            user_media_pair.append(temp)
            temp=[]
        else:
            temp.append(i)
    if temp:
        user_media_pair.append(temp)
    """"
    for i in range(1,len(user_media),2):
        print(user_media[i])
        user_media_pair.append([user_media[i-1],user_media[i]])

        if i%2==1:
            user_media_pair.append([user_media[len(user_media)-1],None])
    if len(user_media)%2==1:
        user_media_pair.append([user_media[len(user_media)-1],None])
    """
    print(user_media_pair)
    subscription = []
    total_cost = 0
    for sub in DisplaysAd.objects.all():
        if sub.ad.username == request.user:
            cost = pricing[sub.screen.type]
            subscription.append((sub, cost))
            total_cost+=cost
    return render(request, "Advertiser/index.html",
                  {'user': str(request.user).split("@")[0],
                   'f1': form,
                   'AdMedia': user_media_pair,
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
    Screen = [(i,(i.ad_available>0)) for i in Screens.objects.all()]
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

    for screen,_ in Screen:
        # print(screen.address,screen.landmarks,search)
        if (search in screen.address) or (search in screen.landmarks):
            if screen_size_filter_flag:
                size = screen.type
                if size == 'Big' and big_size_flag:
                    query_result.append((screen,_))
                elif size == 'Small' and sml_size_flag:
                    query_result.append((screen,_))
                elif size == 'Medium' and med_size_flag:
                    query_result.append((screen,_))
                else:
                    continue
            else:
                query_result.append((screen,_))
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

    if screen.type == 'Big':
        cost = 100

    elif screen.type == 'Small':
        cost = 25

    else:
        cost = 50

    param_dict={
        'MID': 'WorldP64425807474247',
        'ORDER_ID': str(ad_id),
        'TXN_AMOUNT': str(cost),
        'CUST_ID': str(ad_id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/adv/handlerequest',
    }

    param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict, MERCHANT_KEY)

    return render(request, 'Advertiser/paytm.html', {'param_dict': param_dict})


@csrf_exempt
def handlerequest(request):

    return HttpResponse('done')
    pass


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
def notify(request):
    screen_id = request.GET.get('id','')
    if not screen_id:
        return HttpResponse('error')
    user = request.user
    try:

        screen = Screens.objects.get(auto_id=screen_id)
    except Screens.DoesNotExist:
        return HttpResponse('error')
    try:
        x=Waitlist.objects.get(user_waiting=user, screen=screen)
    except Waitlist.DoesNotExist:

        waitlist_obj = Waitlist()
        waitlist_obj.user_waiting = user
        waitlist_obj.screen = screen
        waitlist_obj.save()
        send_mail('Adware', 'You will be notified if screen becomes empty', EMAIL_HOST_USER, [user], fail_silently=False)
        return HttpResponse('success')

    return HttpResponse('already')


def delete_ads(request):
    id = request.GET.get('id','')
    if id:
        try:
            ad_object = AdMedia.objects.get(id=id)
        except AdMedia.DoesNotExist:
            return redirect('/adv')
        active_subscriptions = DisplaysAd.objects.filter(ad=ad_object)
        print(active_subscriptions)
        if not active_subscriptions and ad_object.username == request.user:

            ad_object.delete()
            return redirect("/adv?info=Ad deleted&msgtype=success")

    return redirect("/adv?info=Ad couldn't be deleted&msgtype=error")

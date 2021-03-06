from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdMediaForm
from .models import AdMedia, DisplaysAd,Subscription
from Screens.models import Screens, Waitlist, WaitCount, ScreenCost, ScreenStats
from Screens.views import get_cost_inner , calculate_cost
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
import random
import string
import pickle
from django.core.mail import send_mail
from Adware.settings import EMAIL_HOST_USER

MERCHANT_KEY = 'GvYRwo%@Vl2Ml19y'


"""
Note: put login required decorator for all functions
"""

pricing = {'Big': 100, "Medium": 50, "Small": 30}


@login_required
def index(request):
    schedule_expire_call()
    schedule_cost_queue()
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
    #print(user_media_pair)
    #print(temp)
    subscription = []
    for sub in DisplaysAd.objects.all():
        if sub.ad.username == request.user:
            subscription.append((sub.ad.file_name,sub.screen.type,sub.screen.description))
    return render(request, "Advertiser/index.html",
                  {'user': str(request.user).split("@")[0],
                   'f1': form,
                   'AdMedia': user_media_pair,
                   'temp' : temp,
                   'info': msg,
                   'msgtype': msgtype,
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
    schedule_cost_queue()
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
    #calculate_cost(request)
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



    for x in range(10):
        # print 10 random values between
        # 1 and 100 which are multiple of 5
        ra = ''.join([random.choice(string.ascii_letters
                                        + string.digits) for n in range(15)])

    print(screen_id)
    cost = get_cost_inner(screen.auto_id)
    sub_obj = Subscription(gateway_id=str(ra),screen=screen,ad=ad,cost=cost)
    sub_obj.save()
    print('subcription_id',sub_obj.transaction_id)
    param_dict={
        'MID': 'BiDzIl44175596745392',
        'ORDER_ID': str(ra),
        'TXN_AMOUNT': str(cost),
        'CUST_ID': str(screen_id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/adv/handlerequest/'+str(sub_obj.transaction_id),
    }

    param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict, MERCHANT_KEY)

    return render(request, 'Advertiser/paytm.html', {'param_dict': param_dict})


@csrf_exempt
def handlerequest(request, transaction_id):
    # paytm will send you post request here
    try:
        sub_obj = Subscription.objects.get(transaction_id=transaction_id)
    except Subscription.DoesNotExist:
        print("Invalid Subscription ID")
        return redirect('/adv')

    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    screen = sub_obj.screen
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01' and screen.ad_available>0:
            ad = sub_obj.ad
            disAd = DisplaysAd(screen=screen,ad=ad)
            disAd.save()
            sub_obj.transaction_status = "Transaction Successful"
            sub_obj.save()
            screen.ad_available = screen.ad_available - 1
            screen.save()
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'Advertiser/paymentstatus.html', {'response': response_dict})



def expire():
    if True:
        expiration_time = 4    # days
        query = DisplaysAd.objects.all()
        for obj in query:
            age = timezone.now() - obj.date_created
            print(age,age.days)
            if age.days >= expiration_time:
                screen = obj.screen
                screen.ad_available = screen.ad_available + 1
                screen.save()
                obj.delete()


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
        #send_mail('Adware', 'You will be notified if screen becomes empty', EMAIL_HOST_USER, [user], fail_silently=False)
        return HttpResponse('success')

    return HttpResponse('already')


@login_required
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

@login_required
def all_subscription(request):
    subs = Subscription.objects.filter(ad__username__in=[request.user]).order_by('-transaction_id')
    return render(request, "Advertiser/subs.html", {"subs":subs})


def schedule_expire_call():

    return

def schedule_cost_queue():
    print("Cost Queue")
    gap_time = 1 # 1 minute
    function_call_flag = False
    try:
        fin=open('queue_time.dat','rb')
        last_call = pickle.load(fin)
        fin.close()
        time_now = datetime.now()
        gap = (time_now - last_call).seconds
        gap = gap // 60
        print(type(gap),gap)
        if gap >= gap_time:
            function_call_flag = True
    except FileNotFoundError:
        function_call_flag = True
    print(function_call_flag,gap)
    if function_call_flag:
        calculate_cost()
        fout = open('queue_time.dat','wb')
        time_now = datetime.now()
        pickle.dump(time_now,fout)
        fout.close()
        print("Function Executed")


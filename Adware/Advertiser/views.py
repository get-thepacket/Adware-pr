from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdMediaForm
from .models import AdMedia
from django.http import HttpResponse
from django.conf import settings


"""
Note: put login required decorator for all functions
"""


@login_required
def index(request):
    form = AdMediaForm()

    return render(request, "Advertiser/index.html", {'user':request.user,'f1':form})


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

            return redirect('/adv')

    return render(request, "Advertiser/new_ad.html", {'form': AdMediaForm()})


@login_required
def view_media(request):
    """
    Function to view all uploaded media to the server.
    """

    user_media = AdMedia.objects.filter(username=request.user)

    return render(request, "Advertiser/view_media.html", {'AdMedia': user_media})


@login_required
def media(request, media_name):
    """
    Function to securely access media files
    """

    files = [str(i.media) for i in AdMedia.objects.filter(username=request.user)]

    if media_name not in files:

        return HttpResponse('Unauthorised', status=401)

    img = open(settings.BASE_DIR+'/media/'+media_name,'rb')

    return HttpResponse(img.read(), content_type="image/jpeg")


@login_required
def screen_select(request, ad_id):
    """
    function implements screen selections portal
    ad_id from get request
    todo: user interactive page
    todo: geo-location based selection
    """
    return HttpResponse(str(ad_id))

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdMediaForm
from .models import AdMedia


"""
Note: put login required decorator for all functions
"""


@login_required
def index(request):
    return render(request, "Advertiser/index.html")


@login_required
def new_adv(request):
    if request.method == 'POST':
        obj = AdMedia()
        form = AdMediaForm(request.POST, request.FILES, instance=obj)
        print(form.errors)
        print(form.is_valid())
        if form.is_valid():
            obj.username = request.user
            obj.save()
            return redirect('../')

    return render(request, "Advertiser/new_ad.html", {'form': AdMediaForm()})

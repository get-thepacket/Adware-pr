from django.shortcuts import render


def index(request):
    print("asdfadsf")
    return render(request, "Advertiser/index.html")

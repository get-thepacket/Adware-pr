from django.shortcuts import render
from django.contrib.auth.decorators import login_required


"""
Note: put login required decorator for all functions
"""

@login_required
def index(request):
    return render(request, "Advertiser/index.html")




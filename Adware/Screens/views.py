from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, "Screens/index.html")


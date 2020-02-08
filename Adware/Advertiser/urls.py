from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/new_ad', views.new_adv)

]

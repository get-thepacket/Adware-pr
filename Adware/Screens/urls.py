from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/new/', views.new_scr),
    path('/dis',views.display),
    path('/get-cost', views.get_cost),
]

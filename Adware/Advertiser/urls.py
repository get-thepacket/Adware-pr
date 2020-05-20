from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/new/', views.new_adv),
    path('/view', views.view_media),
    path('/publish/<ad_id>', views.screen_select)
]

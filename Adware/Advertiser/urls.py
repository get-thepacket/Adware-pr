from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/new/', views.new_adv),
    path('/view', views.view_media),
    path('/publish/<ad_id>', views.screen_select),
    path('/publish/<ad_id>/<screen_id>', views.publish),
    path('/exp', views.expire),
    path('/handlerequest/<screen_id>', views.handlerequest),
    path('/wait', views.notify),
    path('/delete', views.delete_ads),
]

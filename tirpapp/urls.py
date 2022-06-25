from django.urls import *
from . import views

urlpatterns=[
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('success',views.success),
    path('logout',views.logout),
    path('newwish',views.new_wish),
    path('stats',views.stats),
    path('create_wish',views.create_wish),
    path('wish/<wish_id>/edit',views.editwish),
    path('wish/<wish_id>/update',views.udpdate_wish),
    path('wish/<wish_id>/destroy',views.wish_destroy),
    path('wish/granted/<wish_id>',views.grant_wish),
    path('wish/<granted_id>/like',views.granted_like)

    
    
    
]
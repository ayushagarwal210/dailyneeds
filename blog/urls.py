from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.bloghome,name='bloghome'),
    path('poscomment',views.postcomment,name='postcomment'),
    path('<str:slug>',views.post,name='post'),
]
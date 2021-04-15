from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.bloghome,name='bloghome'),
    path('postcomment',views.postcomment,name='postcomment'),
    path('addpost',views.addpost,name='addpost'),
    path('<str:slug>',views.post,name='post'),
]
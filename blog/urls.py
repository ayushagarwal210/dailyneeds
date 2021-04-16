from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.bloghome,name='bloghome'),
    path('postcomment',views.postcomment,name='postcomment'),
    path('addpost',views.addpost,name='addpost'),
    path('allposts',views.allposts,name='allposts'),
    path('delete/<post_id>',views.deletepost,name='delete'),
    path('edit/<post_id>',views.editpost,name='edit'),
    path('<str:slug>',views.post,name='post'),
]
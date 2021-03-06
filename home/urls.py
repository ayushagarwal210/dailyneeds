from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('checkout',views.checkout,name='checkout'),
    path('contact',views.contact,name='contact'),
    path('search',views.search,name='search'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('login',views.handleLogin,name='handleLogin'),
    path('logout',views.handleLogout,name='handleLogout'),
    path('cart',views.cart,name='cart'),
    path('order',views.order_view,name='order'),
    path('itemcomment',views.itemcomment,name='itemcomment'),
    path('<str:slug>',views.item,name='item'),
]
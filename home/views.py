from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact,Item
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    allItems=Item.objects.all()
    context={'allItems' : allItems}
    return render(request,'home/home.html',context)

def about(request):
    return HttpResponse('this is about') 

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        feedback=request.POST['feedback']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(feedback)<4:
            messages.error(request,"Please fill form correctly")
        else:
            contact=Contact(name=name, phone=phone, email=email, feedback=feedback)
            contact.save()
            messages.success(request,"Form Submitted")
    return render(request,'home/contact.html')

def item(request,slug):
    item= Item.objects.filter(slug=slug).first()
    context={'item':item}
    return render(request,'home/item.html',context)

def search(request):
    search=request.GET['search']
    if len(search)>78:
        allItems=Item.objects.none();
    else:
        allItems=Item.objects.filter(name__icontains=search)
    if allItems.count()==0:
        messages.warning(request,"No Search Results Found")   
    context={'allItems':allItems,'search':search}
    return render(request,'home/search.html',context)

def handleSignup(request):
    if request.method=='POST':
        username=request.POST['username']
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # Check Error
        if len(phone)<10:
            messages.error(request,"Invalid Phone Number")
            return redirect('/')

        if pass1!=pass2:
            messages.error(request,"Enter Same Password")
            return redirect('/')

        # Create new Account
        myUser=User.objects.create_user(username,email,pass1)
        myUser.name=name
        myUser.phone=phone
        myUser.save()
        messages.success(request,"Account Successfully Created")
        login(request,myUser)
        return redirect('/')

    else:
        return HttpResponse('404-not found')

def handleLogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username = loginusername, password = loginpassword)
        if user is not None: 
            login(request,user)
            messages.success(request,"Successfully loggedin")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/')
    else:
        return HttpResponse("404 not found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')

    

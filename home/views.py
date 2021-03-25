from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from .models import Contact,Item,Order
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    allItems=Item.objects.all()
    context={'allItems' : allItems}
    print(request.session.get('user_id'))
    if request.method=='POST':
        item=request.POST.get('item')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(item)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(item)
                    else:
                        cart[item]=quantity-1
                else:
                    cart[item]=quantity+1
            else:
                cart[item]=1
        else:
            cart={}
            cart[item]=1

        request.session['cart']=cart
        # print(request.session['cart'])
        # print(user_email)
        return redirect('/')
        
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
        request.session['user_id']=user.id
        request.session['user_email']=user.email
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
            request.session['user_id']=user.id
            request.session['user_email']=user.email
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

def cart(request):
    ids=list(request.session.get('cart').keys())
    if ids is not None:
        items=Item.get_product_by_id(ids)
    return render(request,'home/cart.html', {'items':items})
    

def checkout(request):
    if request.method=='POST':
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        user=request.session.get('user_id')
        cart=request.session.get('cart')
        items=Item.get_product_by_id(list(cart.keys()))
        print(address,phone,user,cart,items)

        for item in items:
            order=Order(user=User(id=user),item=item,price=item.price,quantity=cart.get(str(item.id)),address=address,phone=phone)
            print(order)
            order.save()
        request.session['cart']={}
        return redirect('/cart')

def order_view(request):
    user=request.session.get('user_id')
    orders=Order.get_order_by_user(user)
    # print(orders)
    orders=orders.reverse()
    return render(request,'home/order.html',{'orders':orders})
    

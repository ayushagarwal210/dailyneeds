from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from home.models import Contact,Item,Order,ItemComment
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    allItems=Item.objects.all()
    context={'allItems' : allItems}
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
        return redirect('/')
        
    return render(request,'home/home.html',context)

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
    comments=ItemComment.objects.filter(item=item,parent=None)
    replies=ItemComment.objects.filter(item=item).exclude(parent=None)
    replydict={}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno]=[reply]
        else:
            replydict[reply.parent.sno].append(reply)
    context={'item':item,'comments':comments,'user':request.user,'replydict':replydict}
    return render(request,'home/item.html',context)

def search(request):
    search=request.GET['search']
    if len(search)>78:
        allItems=Item.objects.none();
    else:
        allItems=Item.objects.filter(name__icontains=search)
        allPostTitle=Post.objects.filter(title__icontains=search)
        allPostContent=Post.objects.filter(content__icontains=search)
        allPosts=allPostTitle.union(allPostContent)
    if allItems.count()==0:
        messages.warning(request,"No Search Results Found")   
    context={'allItems':allItems,'search':search,'allPosts':allPosts}
    return render(request,'home/search.html',context)

def handleSignup(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        phone=request.POST['phone']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # Check Error
        counter=0
        username=firstname.lower()+"_" +str(counter)
        if User.objects.filter(username=username):
            counter=counter+1
            username=firstname.lower()+"_" +str(counter)
            
        if len(phone)<10:
            messages.error(request,"Invalid Phone Number")
            return redirect('/')

        if pass1!=pass2:
            messages.error(request,"Enter Same Password")
            return redirect('/')

        # Create new Account
        myUser=User.objects.create_user(username,email,pass1)
        myUser.first_name=firstname
        myUser.last_name=lastname
        myUser.save()
        messages.success(request,"Account Successfully Created")
        login(request,myUser)
        request.session['user_id']=myUser.id
        request.session['user_email']=myUser.email
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

@login_required
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')

def cart(request):
    session_cart_variables=request.session.get('cart')
    ids,items=None,[]
    if session_cart_variables is not None:
        ids=list(session_cart_variables.keys())
    
    if ids is not None:
        items=Item.get_product_by_id(ids)
    return render(request,'home/cart.html', {'items':items})
    
@login_required
def checkout(request):
    if request.method=='POST':
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        user=request.session.get('user_id')
        cart=request.session.get('cart')
        items=Item.get_product_by_id(list(cart.keys()))

        for item in items:
            order=Order(user=User(id=user),item=item,price=item.price,quantity=cart.get(str(item.id)),address=address,phone=phone)
            order.save()
        messages.success(request,"Order Placed")
        request.session['cart']={}
        return redirect('/cart')

@login_required
def order_view(request):
    user=request.session.get('user_id')
    orders=Order.get_order_by_user(user)
    orders=orders.reverse()
    return render(request,'home/order.html',{'orders':orders})

def itemcomment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        item_id=request.POST.get("item_id")
        item=Item.objects.get(id=item_id)
        parentsno=request.POST.get('parentsno')
        if parentsno=="":
            comment=ItemComment(comment=comment,user=user,item=item)
            messages.success(request,"Comment Posted")
        else:
            parent=ItemComment.objects.get(sno=parentsno)
            comment=ItemComment(comment=comment,user=user,item=item,parent=parent)      
            messages.success(request,"Reply Posted")
        comment.save()
    return redirect(f"/{item.slug}")
    

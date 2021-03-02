from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact,Item

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
        contact=Contact(name=name, phone=phone, email=email, feedback=feedback)
        contact.save()
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
    context={'allItems':allItems,'search':search}
    return render(request,'home/search.html',context)

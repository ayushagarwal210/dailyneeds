from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

# Create your views here.
def bloghome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def post(request,slug):
    return HttpResponse(f"{slug}")

def postcomment(request):
    return HttpResponse("post")
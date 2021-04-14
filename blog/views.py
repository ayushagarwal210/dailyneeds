from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post

# Create your views here.
def bloghome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def post(request,slug):
    post=Post.objects.filter(slug=slug).first()
    context={'post':post}
    return render(request,'blog/blogPost.html',context)

def postcomment(request):
    return HttpResponse("post")
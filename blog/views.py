from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog.models import Post,BlogComment
from django.contrib import messages

# Create your views here.
def bloghome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)

def post(request,slug):
    post=Post.objects.filter(slug=slug).first()
    comments=BlogComment.objects.filter(post=post,parent=None)
    context={'post':post,'comments':comments}
    return render(request,'blog/blogPost.html',context)

def postcomment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get("postsno")
        post=Post.objects.get(id=postsno)
        comments=BlogComment(comment=comment,user=user,post=post)
        comments.save()
        messages.success(request,"Comment Posted")
    return redirect(f"/blog/{post.slug}")

def addpost(request):
    if request.method=='POST':
        title=request.POST.get('title')
        author=request.user
        content=request.POST.get('content')
        slug=request.POST.get('slug')
        post=Post(title=title,author=author,content=content,slug=slug)
        post.save()
        messages.success(request,"Posted successfully")
    return render(request,'blog/addPost.html')
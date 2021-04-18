from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from blog.models import Post,BlogComment
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def addpost(request):
    if request.method=='POST':
        title=request.POST.get('title')
        author=request.user
        content=request.POST.get('content')
        post=Post(title=title,author=author,content=content)
        post.save()
        messages.success(request,"Posted successfully")
    return render(request,'blog/addPost.html')

@login_required
def allposts(request):
    post_user=Post.objects.filter(author=request.user)
    return render(request,'blog/allPosts.html',{'post_user':post_user})

@login_required
def deletepost(request,post_id=None):
    if request.user==Post.author:
        post_to_delete=Post.objects.get(id=post_id)
        post_to_delete.delete()
        messages.success(request,"Post Deleted Successfully")
    else:
        return HttpResponse("404 error")
    return redirect("/blog/allposts")

@login_required
def editpost(request,post_id=None):
    if request.user==Post.author:
        post_to_edit=Post.objects.get(id=post_id)
        if request.method=='POST':    
            post_to_edit.title=request.POST.get('title')
            post_to_edit.content=request.POST.get('content')
            post_to_edit.save()
            messages.success(request,"Post Edited")
    else:
        return HttpResponse("404 error")
    return render(request,'blog/editPost.html',{'post_to_edit':post_to_edit})
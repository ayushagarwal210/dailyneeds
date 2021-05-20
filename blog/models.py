from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    slug=models.SlugField(max_length=500,unique=True,blank=True)
    timestamp=models.DateTimeField(default=now)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)+"-"+slugify(self.timestamp)+"-"+slugify(self.author)
        super().save(*args,**kwargs)


class BlogComment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)


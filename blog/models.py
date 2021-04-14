from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    slug=models.CharField(max_length=255)
    timestamp=models.DateTimeField(default=now)
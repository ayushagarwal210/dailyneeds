from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=300)
    phone=models.CharField(max_length=13)
    feedback=models.TextField()
    email=models.EmailField(max_length=255)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name=models.CharField(max_length=300)
    price=models.IntegerField()
    category=models.CharField(max_length=20,default=None)
    image=models.ImageField(upload_to='images/',blank=True,null=True)
    description=models.TextField()
    store=models.CharField(max_length=300)
    timestamp=models.DateTimeField()
    slug=models.CharField(max_length=30)

    @staticmethod
    def get_product_by_id(ids):
        return Item.objects.filter(id__in=ids)

    def __str__(self):
        return self.name+' by '+self.store


class Order(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField(default=None,blank=True)
    address=models.CharField(max_length=100,default='')
    phone=models.CharField(max_length=10,default='')
    timestamp=models.DateTimeField(default=now)
    status=models.BooleanField(default=False)

    @staticmethod
    def get_order_by_user(user_id):
        return Order.objects.filter(user=user_id).order_by('timestamp')
    
    def __str__(self):
        return self.user.username+" "+self.item.name[0:25]+" quantity- "+str(self.quantity)

class ItemComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:20]+"..."+" by "+self.user.username
    
    

    
    

    

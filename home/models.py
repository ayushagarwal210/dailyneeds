from django.db import models

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
    description=models.TextField()
    store=models.CharField(max_length=300)
    timestamp=models.DateTimeField()
    slug=models.CharField(max_length=30)

    def __str__(self):
        return self.name+'by'+self.store
    

    

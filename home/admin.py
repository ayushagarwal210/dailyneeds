from django.contrib import admin
from .models import Contact,Item,Order,ItemComment

# Register your models here.
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register((Item,ItemComment))
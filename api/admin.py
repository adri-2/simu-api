from django.contrib import admin
from .models import Category,ImportSimulation,Product,UserInfo

# Register your models here.
admin.site.register(Category)
admin.site.register(ImportSimulation)
admin.site.register(Product)
admin.site.register(UserInfo)
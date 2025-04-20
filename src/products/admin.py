from django.contrib import admin

# Register your models here.
# admin.py
from .models import Product, Brand

admin.site.register(Product)
admin.site.register(Brand)
from django.contrib import admin
from .models import VendorInformation, MenuItems, Category

# Register your models here.
admin.site.register((VendorInformation, MenuItems, Category))

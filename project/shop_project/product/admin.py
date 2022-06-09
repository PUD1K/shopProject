from django.contrib import admin

from .models import Manufacturer, Product, Category, Subcategory, Comments

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Manufacturer)
admin.site.register(Comments)
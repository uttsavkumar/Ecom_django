from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


class CategoryDesc(admin.ModelAdmin):
    search_fields = ['id','slug']
    def delete_button(self,obj):
        return format_html('<a href="/admin/shop/category/{}/delete">Delete</a>',obj.id)
    def update_button(self,obj):
        return format_html('<a href="/admin/shop/category/{}/change">Edit</a>',obj.id)
    
    list_display = ['id','title','slug','delete_button','update_button']

    prepopulated_fields = {'slug':('title',)}


class ProductDesc(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category,CategoryDesc)
admin.site.register(Product,ProductDesc)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Address)
admin.site.register(Payment)
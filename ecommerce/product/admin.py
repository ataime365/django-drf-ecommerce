from django.contrib import admin

from .models import Brand, Category, Product, ProductLine


class ProductLineInline(admin.TabularInline): #using TabularInline
    """ProductLine is a Child Model to Product"""
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductLineInline,
    ]


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductLine) #Not needed, but just incase we want to see the ProductLine separately
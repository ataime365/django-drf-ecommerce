from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Brand, Category, Product, ProductLine, ProductImage


class EditLinkInline(object): #images
    """instance here is the instance of the ProductLine we are working with"""
    def edit(self, instance):
        """edit , edits the whole product line, not just product images"""
        url = reverse(f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
                      args=[instance.pk], )

        if instance.pk:
            # If instance exists, show the edit button
            link = mark_safe(f'<a href={url}>edit</a>')
            return link
        else:
            return ""


class ProductImageInline(admin.TabularInline):
    """ProductImage is a child Model to ProductLine"""
    model = ProductImage


class ProductLineInline(EditLinkInline, admin.TabularInline): #using TabularInline
    """ProductLine is a Child Model to Product"""
    model = ProductLine
    readonly_fields = ("edit",) #"edit" from the edit function above


# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductLineInline
    ]

class ProductLineAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductLine, ProductLineAdmin)

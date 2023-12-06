from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductLine, ProductImage, AttributeValue, Attribute, ProductType
# We are only importing real tables and no intermediate tables


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


class AttributeValueProductLineInline(admin.TabularInline):
    """ ProductLine to AttributeValue
    On the ProductLine table, we have a M2M reference field -> attribute_value = models.ManyToManyField(to=AttributeValue, 
                                             through="ProductLineAttributeValue", 
                                             related_name="product_line_attribute_value") """
    model = AttributeValue.product_line_attribute_value.through #This points to the "ProductLineAttributeValue" intermediate model

class AttributeValueProductInline(admin.TabularInline):
    """Product to AttributeValue"""
    model = AttributeValue.product_attribute_value.through

# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductLineInline,
        AttributeValueProductInline
    ]

class ProductLineAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        AttributeValueProductLineInline,
    ]

class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through # Points to "ProductTypeAttribute" intermediate model #many-to-many reference
            #SecondTable.related_name_from_m2m_on_FirstTable.through

class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeInline,
    ]

class AttributeAdmin(admin.ModelAdmin):
    """Added this myself, not very important"""
    ordering = ('id',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductLine, ProductLineAdmin) #utilizing customizations
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeValue)
admin.site.register(ProductType, ProductTypeAdmin)



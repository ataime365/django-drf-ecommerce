from collections.abc import Collection, Iterable
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError

class ActiveQueryset(models.QuerySet): #models.Manager , no need for managers
    """This Model Manager enables us return Active Products and Product Lines,
    We also need to apply the Manager to the Model after creating it
    default Manager = objects (From django ORM)
    """
    # def isactive(self): #models.Manager 
    #     """This makes this function callable, we are not overriding anything"""
    #     return self.get_queryset().filter(is_active=True)
    def isactive(self): 
        return self.filter(is_active=True)

class Category(MPTTModel):
    """Overall, this Category model is designed to store hierarchical data, 
    Where each sub category can have a parent category, except for the top-level categories. 
    This structure is common in scenarios where categories have subcategories, 
    and subcategories can have their own subcategories, forming a tree-like hierarchy."""   
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        """This is what will show in the Admin Interface, debugging e.t.c"""
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    """A product must have a brand, but category is not compulsory, can be null"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255) #we can't have 2 product with the same url, so the slug link has to be unique
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False) #Most of the products are physical products
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) #use SET_NULL # the on_delete is for the brand, if the brand is deleted
    category = TreeForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()  #When not overriding anything
    # objects = ActiveManager() #when using #models.Manager #When not overriding anything 

    def __str__(self):
        return self.name
    

class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=6)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line" #used for reverse relationships in serializers.py
        )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product" , blank=True)

    objects = ActiveQueryset.as_manager() #There is at least one Model manager for each model, default is objects, we have customized the default

    def clean(self):
        """This filters for duplicate order number"""
        # super().clean_fields(exclude=exclude)
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")
            
    def save(self, *arg, **kwargs):
        """To make sure the clean() method above is always called"""
        self.full_clean()
        return super(ProductLine, self).save(*arg, **kwargs)

    def __str__(self):
        return str(self.sku)


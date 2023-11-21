from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Overall, this Category model is designed to store hierarchical data, 
    Where each sub category can have a parent category, except for the top-level categories. 
    This structure is common in scenarios where categories have subcategories, 
    and subcategories can have their own subcategories, forming a tree-like hierarchy."""   
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        """This is what will show in the Admin Interface, debugging e.t.c"""
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

    def __str__(self):
        return self.name
    

class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=6)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line" #used for reverse relationships
        )
    is_active = models.BooleanField(default=False)


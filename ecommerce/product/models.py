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
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False) #Most of the products are physical products
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) #use SET_NULL
    category = TreeForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    


from collections.abc import Collection, Iterable
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError

class IsActiveQueryset(models.QuerySet): #models.Manager , no need for managers
    """This Model Manager enables us return Active Products and Product Lines,
    We also need to apply the Manager to the Model after creating it
    default Manager = objects (From django ORM)
    """
    # def isactive(self): #models.Manager 
    #     """This makes this function callable, we are not overriding anything"""
    #     return self.get_queryset().filter(is_active=True)
    def is_active(self): 
        return self.filter(is_active=True)


class Category(MPTTModel):
    """Overall, this Category model is designed to store hierarchical data, 
    Where each sub category can have a parent category, except for the top-level categories. 
    This structure is common in scenarios where categories have subcategories, 
    and subcategories can have their own subcategories, forming a tree-like hierarchy."""   
    name = models.CharField(max_length=235, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = IsActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        """This is what will show in the Admin Interface, debugging e.t.c"""
        return self.name
    

class Product(models.Model):
    """A product must have a brand, but category is not compulsory, can be null"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255) #we can't have 2 product with the same url, so the slug link has to be unique
    pid = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False) #Most of the products are physical products
    category = TreeForeignKey("Category", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    product_type = models.ForeignKey("ProductType", on_delete=models.PROTECT, related_name="product")
    created_at = models.DateTimeField(auto_now_add=True, editable=False) #auto_now_add adds the time and date field #editable=False it wouldnt be shown in the admin
    # M2M reference
    attribute_value = models.ManyToManyField(to="AttributeValue", 
                                             through="ProductAttributeValue", 
                                             related_name="product_attribute_value") #related_name already in use ?
    
    objects = IsActiveQueryset.as_manager()  #When not overriding anything
    # objects = ActiveManager() #when using #models.Manager #When not overriding anything 

    def __str__(self):
        return self.name
    

class Attribute(models.Model):
    """Example: 'mens-shoe-size', 'mens-shoe-color' """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """Example: 11, 12, 13 Or blue, green """
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value" #class name
    )

    def __str__(self):
        return self.attribute.name + '-' + self.attribute_value
    

class ProductAttributeValue(models.Model):
    """This is the intermediate table that resolves 
    the 1 'many-to-many' relationship into two(2) 'one-to-many' relationships ,
    using 2 foreign keys from each table"""
    attribute_value = models.ForeignKey(
        AttributeValue, on_delete=models.CASCADE, related_name="product_attribute_value_av"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_attribute_value_pl"
    )

    class Meta:
        """The two values should be unique together"""
        unique_together = ("attribute_value", "product")

    def clean(self):
        """Validation Check: Ensure that each attribute type is unique per product line."""
        if ProductAttributeValue.objects.filter(
            product=self.product,
            attribute_value__attribute=self.attribute_value.attribute
        ).exclude(id=self.id).exists(): 
            #exclude , excludes the current instance of ProductLineAttributeValue (intermediate table), 
            # so the current instance isn't flaggged as a duplicate
            raise ValidationError(f"Duplicate attribute type for {self.product}.")

    def save(self, *args, **kwargs):
        """To ensure the clean method is called."""
        self.full_clean()
        super(ProductAttributeValue, self).save(*args, **kwargs)


class ProductLineAttributeValue(models.Model):
    """This is the intermediate table that resolves 
    the 1 'many-to-many' relationship into two(2) 'one-to-many' relationships ,
    using 2 foreign keys from each table"""
    attribute_value = models.ForeignKey(
        AttributeValue, on_delete=models.CASCADE, related_name="product_line_attribute_value_av"
    )
    product_line = models.ForeignKey(
        "ProductLine", on_delete=models.CASCADE, related_name="product_line_attribute_value_pl"
    )

    class Meta:
        """The two values should be unique together"""
        unique_together = ("attribute_value", "product_line")

    def clean(self):
        """Validation Check: Ensure that each attribute type is unique per product line."""
        if ProductLineAttributeValue.objects.filter(
            product_line=self.product_line,
            attribute_value__attribute=self.attribute_value.attribute
        ).exclude(id=self.id).exists(): 
            #exclude , excludes the current instance of ProductLineAttributeValue (intermediate table), 
            # so the current instance isn't flaggged as a duplicate
            raise ValidationError(f"Duplicate attribute type for {self.product_line}.")

    def save(self, *args, **kwargs):
        """To ensure the clean method is called."""
        self.full_clean()
        super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=6)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="product_line" #used for reverse relationships in serializers.py
        )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product" , blank=True)
    weight = models.FloatField()

    attribute_value = models.ManyToManyField(to=AttributeValue, 
                                             through="ProductLineAttributeValue", 
                                             related_name="product_line_attribute_value") 
    #attribute_value is just a reference, and not an actual value stored in the database
    created_at = models.DateField(auto_now_add=True, editable=False)
    product_type = models.ForeignKey("ProductType", on_delete=models.PROTECT, related_name="product_line_type")

    objects = IsActiveQueryset.as_manager() #There is at least one Model manager for each model, default is objects, we have customized the default

    def clean(self):
        """This filters for duplicate order number. #order"""
        # super().clean_fields(exclude=exclude)
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")
            
    def save(self, *arg, **kwargs):
        """To make sure the clean() method above is always called. #order"""
        self.full_clean()
        return super(ProductLine, self).save(*arg, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image" #used for reverse relationships in serializers.py
        )
    order = OrderField(unique_for_field="product_line" , blank=True)

    def clean(self):
        """This filters for duplicate order number. #order"""
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")
            
    def save(self, *arg, **kwargs):
        """To make sure the clean() method above is always called. #order"""
        self.full_clean()
        return super(ProductImage, self).save(*arg, **kwargs)

    def __str__(self):
        return f"{self.product_line.sku}_img" #using the foreign key to traverse to the ProductLine table to access the sku 


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    # This reference is used in the Tabular Inline in the admin.py
    attribute = models.ManyToManyField(to=Attribute, 
                                             through="ProductTypeAttribute", 
                                             related_name="product_type_attribute") #many-to-many reference
    
    def __str__(self):
        return self.name

class ProductTypeAttribute(models.Model):
    """This is the intermediate table that resolves 
    the 1 'many-to-many' relationship into two(2) 'one-to-many' relationships ,
    using 2 foreign keys from each table. Connecting ProductType Table to Attribute Table"""
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_type_attribute_pt"
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="product_type_attribute_at"
    )

    class Meta:
        """The two values should be unique together"""
        unique_together = ("product_type", "attribute")


# slug = asus-tuf-gaming-vg249
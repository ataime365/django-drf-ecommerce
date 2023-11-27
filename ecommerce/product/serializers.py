from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name") #mapping "name" to category_name, or changing name #Not neccessary for the ProductSerializer output

    class Meta:
        model = Category
        fields = ["category_name",]


class BrandSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="name") #mapping #Not neccessary for the ProductSerializer output

    class Meta:
        model = Brand
        fields = ["brand_name",]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "productline")


class ProductLineSerializer(serializers.ModelSerializer):
    # product = ProductSerializer() #ForeignKey
    product_image = ProductImageSerializer(many=True) #product_line meant to be product_image, but product_line is the related_field available

    class Meta:
        model = ProductLine
        # exclude = ("id", "product", "is_active") #product here is only showing product_id number
        fields = ["price", "sku", "stock_qty", "order", "product_image"]


class ProductSerializer(serializers.ModelSerializer):
    # brand_name = BrandSerializer()  #To enable brand and category data related to a product to be returned with Products data
    # category_name = CategorySerializer(source="category.name") #Doesnt work
    brand_name = serializers.CharField(source="brand.name") #source Mapping and Flatenning # Only works with serializers.Fields and not with the direct BrandSerializers
    category_name = serializers.CharField(source="category.name") #source Mapping and Flatenning
    product_line = ProductLineSerializer(many=True) # many=True Because one Product can have many product lines #product_line is a related_name

    class Meta:
        model = Product
        # exclude = ("id",)
        fields = ["name", "slug", "description", "is_digital", "brand_name", "category_name", "product_line"]





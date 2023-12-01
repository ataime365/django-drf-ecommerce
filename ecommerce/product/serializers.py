from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine, ProductImage, Attribute, AttributeValue, ProductType


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


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False) #Foreign key
    # attribute = serializers.CharField(source="attribute.name") #Flattening and mapping

    class Meta:
        model = AttributeValue
        fields = ["attribute", "attribute_value"]


class ProductLineSerializer(serializers.ModelSerializer):
    # product = ProductSerializer() #ForeignKey
    product_image = ProductImageSerializer(many=True) #reverse relationships
    attribute_value = AttributeValueSerializer(many=True)  # many-to-many ForeignKey

    class Meta:
        model = ProductLine
        # exclude = ("id", "product", "is_active") #product here is only showing product_id number
        fields = ["price",
                   "sku", 
                   "stock_qty", 
                   "order", 
                   "product_image",
                   "attribute_value" ,#many-to-many reference # The attribute_value above overrides the value of this
                   ]
        
    def to_representation(self, instance):
        """To customize the serializer output, pop() and update() are dictionary methods
        attribute_value_data is a list of dictionaries, we want to convert it to only one dictionary
        SAMPLE DATA
        "attribute_value": [
          {"attribute": {"name": "screen size","id": 1}, 
           "attribute_value": "32"},
          {"attribute": {"name": "panel type","id": 2}, 
          "attribute_value": "IPS"},
          ]"""
        data = super().to_representation(instance) #data is a dictionary/OrderedDict # One record
        attribute_value_data = data.pop("attribute_value") #pop has removed the attribute_value from the whole data, At this point
        attr_values_dict = {}
        for element in attribute_value_data:
            # attr_values_dict[element.get("attribute").get("id")] = element.get("attribute_value") #works fine
            attr_values_dict.update({element.get("attribute").get("name") : element.get("attribute_value")}) #using name is better than id
        # data["specification"] = attr_values_dict #data is a dictionary #works fine
        data.update({"specification": attr_values_dict})
        return data


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ["name", "attribute"]


class ProductSerializer(serializers.ModelSerializer):
    # brand_name = BrandSerializer()  #To enable brand and category data related to a product to be returned with Products data
    # category_name = CategorySerializer(source="category.name") #Doesnt work
    brand_name = serializers.CharField(source="brand.name") #source Mapping and Flatenning # Only works with serializers.Fields and not with the direct BrandSerializers
    category_name = serializers.CharField(source="category.name") #source Mapping and Flatenning
    product_line = ProductLineSerializer(many=True) # many=True Because one Product can have many product lines #product_line is a related_name #reverse relationships foreign key
    # product_type = ProductTypeSerializer()
    attribute = serializers.SerializerMethodField(read_only=True) #This is used to add custom fields that doesnt already exist on our model
    

    class Meta:
        model = Product
        # exclude = ("id",)
        fields = ["name", 
                  "slug", 
                  "description", 
                  "is_digital",
                #   "product_type", 
                  "brand_name", 
                  "category_name", 
                  "product_line",
                  "attribute"]

    def get_attribute(self, obj):
        """custom field: From the SerializerMethodField above, filter by related_name, Always use real tables, never intermediate tables
        This is just like running an SQl query on a joined table"""
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        # print(attribute)
        return AttributeSerializer(attribute, many=True).data


    def to_representation(self, instance):
        """To customize the serializer output, customizing the 'attribute' output"""
        data = super().to_representation(instance)
        attribute_data = data.pop("attribute")
        attribute_dict = {}
        for element in attribute_data:
            attribute_dict.update({element.get("id"): element.get("name")})
        data.update({"type specification": attribute_dict})
        return data
    

# serializers are very important in customizing the data output and manipulating the data
from rest_framework import serializers

from .models import Category, Product, ProductLine, ProductImage, Attribute, AttributeValue, ProductType


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name") #mapping "name" to category_name, or changing name #Not neccessary for the ProductSerializer output

    class Meta:
        model = Category
        fields = ["category", "slug"]



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "product_line")


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
    # brand_name = serializers.CharField(source="brand.name") #source Mapping and Flatenning # Only works with serializers.Fields and not with the direct BrandSerializers
    
    # category = serializers.CharField(source="category.name") #source Mapping and Flatenning
    product_line = ProductLineSerializer(many=True) # many=True Because one Product can have many product lines #product_line is a related_name #reverse relationships foreign key
    # product_type = ProductTypeSerializer()
    # attribute = serializers.SerializerMethodField(read_only=True) #Custom field #This is used to add custom fields that doesnt already exist on our model
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = Product
        # exclude = ("id",)
        fields = ["name", 
                  "slug", 
                  "pid",
                  "description", 
                #   "is_digital",
                #   "product_type", 
                #   "category",
                #   "created_at", 
                  "product_line",
                  "attribute_value"] # first check output from this attribute_value

    # def get_attribute(self, obj):
    #     """custom field: From the SerializerMethodField above, filter by related_name, Always use real tables, never intermediate tables
    #     This is just like running an SQl query on a joined table"""
    #     attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
    #     # print(attribute)
    #     return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        """To customize the serializer output, customizing the 'attribute' output
        attribute is also renamed to 'type specification' """
        data = super().to_representation(instance)
        attribute_data = data.pop("attribute_value")
        attr_values_dict = {}
        for element in attribute_data:
            attr_values_dict.update({element.get("attribute").get("name"): element.get("attribute_value")})
        data.update({"attribute": attr_values_dict})
        return data
    

class ProductLineCategorySerializer(serializers.ModelSerializer):
    """Another ProductLine serializer for a different Task"""
    product_image = ProductImageSerializer(many=True) #reverse relationships

    class Meta:
        model = ProductLine
        fields = ["price",
                   "product_image",
                   ]

class ProductCategorySerializer(serializers.ModelSerializer):
    """Another Product Serializer for a different Task"""
    # category = serializers.CharField(source="category.name") #source Mapping and Flatenning
    product_line = ProductLineCategorySerializer(many=True) # many=True Because one Product can have many product lines #product_line is a related_name #reverse relationships foreign key

    class Meta:
        model = Product
        fields = ["name", 
                  "slug", 
                  "pid",
                #   "category",
                  "created_at", 
                  "product_line"]

    def to_representation(self, instance):
        """To customize the serializer output, customizing the 'Product Category' output"""
        data = super().to_representation(instance)
        x = data.pop("product_line") #x is a list of Product lines, but we are taking only the first one x[0]
        # print(x) #To inspect the data coming from 'list_product_by_category_slug' view
        if x: #To avoid errors
            first_product_line = x[0]
            price = first_product_line["price"]
            image = first_product_line["product_image"]
            data.update({"price":price, "image":image})
            # data.update({"image":image})
        return data


# serializers are very important in customizing the data output and manipulating the data
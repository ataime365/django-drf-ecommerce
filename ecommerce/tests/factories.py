import factory

from ecommerce.product.models import (Category, Product, ProductType, 
                                      ProductLine, Attribute, AttributeValue, 
                                      ProductImage, ProductLineAttributeValue)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    #Fields we want to test
    name = factory.Sequence(lambda n: f"test_category_{n}") #creating varying/dynamic values
    slug = factory.Sequence(lambda n: f"test_slug_{n}") #creating varying/dynamic values
    # is_active = True


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "attribute name test"
    description = "attr description test"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: f"test_product_type_{n}") #Just to make it dynamic
    # parent = factory.SubFactory("self")

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        """For many-to-many references, Not mandatory because there isn't an actual field"""
        if not create or not extracted:
            return
        self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    #Fields we want to test
    name =factory.Sequence(lambda n: f"test_product_name_{n}") #creating varying/dynamic values  "test_Product"
    pid =factory.Sequence(lambda n: f"0000_{n}") #creating varying/dynamic values 
    description = "test_description"
    is_digital = False
    category = factory.SubFactory(CategoryFactory) #Foreign key
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory) #Foreign key

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        """For many-to-many references, Not mandatory because there isn't an actual field"""
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    #Fields
    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    product_type = factory.SubFactory(ProductTypeFactory)
    is_active = True
    weight = 100

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        """For many-to-many references, Not mandatory because there isn't an actual field"""
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = "attr value test"
    attribute = factory.SubFactory(AttributeFactory)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test alternative text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)

    # order is auto generated, no need to test it


class ProductLineAttributeValueFactory(factory.django.DjangoModelFactory):
    """Intermediate Table, not always used, has 2 Foreign Keys"""
    class Meta:
        model = ProductLineAttributeValue

    attribute_value = factory.SubFactory(AttributeValueFactory)
    product_line = factory.SubFactory(ProductLineFactory)
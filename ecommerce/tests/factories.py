import factory

from ecommerce.product.models import (Attribute, AttributeValue,
                                      Brand, Category, 
                                      Product, ProductLine, 
                                      ProductImage, ProductType)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    #Fields we want to test
    name = factory.Sequence(lambda n: f"category_{n}") #creating varying/dynamic values


class BrandFactory(factory.django.DjangoModelFactory): #obj
    class Meta:
        model = Brand

    #Fields we want to test
    name = factory.Sequence(lambda n: f"brand_{n}")


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "attribute name test"
    description = "attr description test"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = "test product type"

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
    name = "test_Product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory) # Creates a brand before the product object is created
    category = factory.SubFactory(CategoryFactory) #Foreign key
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory) #Foreign key


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    #Fields
    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True

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
    productline = factory.SubFactory(ProductLineFactory)

    #order is auto generated, no need to test it



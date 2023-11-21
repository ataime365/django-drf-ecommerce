import factory

from ecommerce.product.models import Brand, Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    #Fields we want to test
    name = factory.Sequence(lambda n: f"category_{n}")


class BrandFactory(factory.django.DjangoModelFactory): #obj
    class Meta:
        model = Brand

    #Fields we want to test
    name = factory.Sequence(lambda n: f"brand_{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    #Fields we want to test
    name = "test_Product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory) # Creates a brand before the product object is created
    category = factory.SubFactory(CategoryFactory)
    is_active = True



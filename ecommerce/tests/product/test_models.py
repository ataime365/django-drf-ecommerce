import pytest
from django.core.exceptions import ValidationError

from ecommerce.product.models import ProductTypeAttribute #Not neccessary

#Gives us access to the db
pytestmark = pytest.mark.django_db #Available globally, no need to design each funtion, 


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
         #Category Model #Data mockup from factories #This is both Arrange and Act
        obj = category_factory(name="test_cat") #To override the data from the factory #This line automatically adds data to the database
        # Assert
        assert obj.__str__() == "test_cat"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        #Arrange
        #Act   #obj used to be x
        obj = brand_factory(name="test_brand") #overriding
        # Assert
        assert obj.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        #Arrange
        #Act   #obj used to be x
        obj = product_factory(name="test_Product") #overriding
        # Assert
        assert obj.__str__() == "test_Product"


class TestProductLineModel:
    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr_v = attribute_value_factory(attribute_value="test") # M2M - many-to-many
        obj = product_line_factory.create(sku="12345", attribute_value=(attr_v, ))
        assert obj.__str__() == "12345"


    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory() # New Product
        product_line_factory(order=1, product=obj) #creating a product line using that product #Fk

        with pytest.raises(ValidationError):
            # same as the line above, and calling the clean() method in addition
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:
    """This factory will initiate/start all the other factories it is connected to"""
    def test_str_method(self, product_image_factory):
        obj = product_image_factory(url="test.jpg") #order=1
        assert obj.__str__() == "test.jpg" # "1"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        attr = attribute_factory(name="test") #M2M many-to-many
        obj = product_type_factory.create(name="test_type", attribute=(attr, ))

        # x = ProductTypeAttribute.objects.filter(id=1)
        # print(x)

        assert obj.__str__() == "test_type"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attribute")
        assert obj.__str__() == "test_attribute"


class TestAttributeValueModel:
    """Because of the string output concatenates 2 things, quite different from the rest, but Not a Many-to_many"""
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute") #output has 2 things obj_a and obj_b
        obj_b = attribute_value_factory.create(attribute_value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute-test_value"



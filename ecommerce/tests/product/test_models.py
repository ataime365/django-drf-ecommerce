import pytest
from django.core.exceptions import ValidationError

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
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="12345")
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





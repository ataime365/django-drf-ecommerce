import pytest

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
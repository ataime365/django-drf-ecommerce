import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ecommerce.product.models import ProductTypeAttribute #Not neccessary
from ecommerce.product.models import Category, Product, ProductLine

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

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = "x" * 256
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="test_cat")
        with pytest.raises(IntegrityError): #Using same category name to test the uniqueness
            category_factory(name="test_cat")

    def test_slug_unique_field(self, category_factory):
        """If the test passes without throwing an error, 
        it means that the context manager successfully caught an IntegrityError as expected. """
        category_factory(slug="test_slug")
        with pytest.raises(IntegrityError): #Using same category slug to test the uniqueness
            category_factory(slug="test_slug")

    def test_is_active_false_default(self, category_factory):
        obj = category_factory()
        assert obj.is_active is False #default setting #we use 'is' for boolean test and not '=='

    def test_parent_category_on_delete_protect(self, category_factory):
        obj1 = category_factory() #These two lines are setting up a parent-child relationship between two category 
        category_factory(parent=obj1)  #This line creates the child category, while obj1 is the parent category
        with pytest.raises(IntegrityError): 
            obj1.delete()

    def test_parent_field_null(self, category_factory):
        obj1 = category_factory() #didnt specify parent
        assert obj1.parent is None

    def test_return_category_active_only_true(self, category_factory):
        """Testing IsActiveQueryset ... object"""
        category_factory(is_active=True) 
        category_factory(is_active=False) #This first 2 linew creates two new categories 
        qs = Category.objects.is_active().count()
        assert qs == 1

    def test_return_category(self, category_factory):
        """Testing Normal behaviour"""
        category_factory(is_active=True) 
        category_factory(is_active=False) #This first 2 linew creates two new categories
        qs = Category.objects.count()
        assert qs == 2



class TestProductModel:
    def test_str_method(self, product_factory):
        obj = product_factory(name="test_Product") #overriding
        assert obj.__str__() == "test_Product"

    def test_name_max_length(self, product_factory):
        name = "x" * 101
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, product_factory):
        slug = "x" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_pid_length(self, product_factory):
        pid = "x" * 11
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_false_default(self, product_factory):
        obj = product_factory(is_digital=False) 
        assert obj.is_digital is False #Testing default

    def test_fk_category_on_delete_protect(self, category_factory, product_factory):
        obj1 = category_factory() 
        product_factory(category=obj1)
        with pytest.raises(IntegrityError): 
            obj1.delete()

    def test_return_product_active_only_true(self, product_factory):
        """Testing IsActiveQueryset ... object"""
        product_factory(is_active=True) 
        product_factory(is_active=False) #This first 2 lines creates two new products 
        qs = Product.objects.is_active().count()
        assert qs == 1

    def test_return_product(self, product_factory):
        """Testing Normal behaviour"""
        product_factory(is_active=True) 
        product_factory(is_active=False) #This first 2 linew creates two new products
        qs = Product.objects.count()
        assert qs == 2


class TestProductLineModel:
    def test_duplicate_attribute_inserts(
            self, product_line_factory, attribute_factory, 
            attribute_value_factory, product_line_attribute_value_factory ):
        """Testing the intermediate table"""
        obj1 = attribute_factory(name="shoe-color")
        obj2 = attribute_value_factory(attribute_value="red", attribute=obj1)
        obj3 = attribute_value_factory(attribute_value="blue", attribute=obj1) #creating 2 attribute values for the same attribute
        obj4 = product_line_factory()
        product_line_attribute_value_factory(attribute_value=obj2, product_line=obj4)

        with pytest.raises(ValidationError):
            product_line_attribute_value_factory(attribute_value=obj3, product_line=obj4).clean()

    def test_str_method(self, product_line_factory, attribute_value_factory):
        attr_v = attribute_value_factory(attribute_value="test") # M2M - many-to-many
        obj = product_line_factory.create(sku="12345", attribute_value=(attr_v, ))
        assert obj.__str__() == "12345"

    def test_fk_product_type_on_delete_protect(self, product_type_factory, product_line_factory):
        """Between product_line and product_type, testing the on_delete PROTECT"""
        obj1 = product_type_factory() 
        product_line_factory(product_type=obj1)
        with pytest.raises(IntegrityError): 
            obj1.delete()

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory() # New Product
        product_line_factory(order=1, product=obj) #creating a product line using that product #Fk

        with pytest.raises(ValidationError):
            # same as the line above, and calling the clean() method in addition
            product_line_factory(order=1, product=obj).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.001 #3 decimal places, the ValidationError should catch this, without throwing an error
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_price_max_digits(self, product_line_factory):
        """Testing max digits allowed 6, make it 7 to test it"""
        price = 10000.00 #should catch this, without throwing an error
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_sku_max_length(self, product_line_factory):
        sku = "x" * 101
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_is_active_false_default(self, product_line_factory):
        obj = product_line_factory(is_active=False) 
        assert obj.is_active is False #Testing default

    def test_fk_product_on_delete_protect(self, product_factory, product_line_factory):
        obj1 = product_factory() 
        product_line_factory(product=obj1)
        with pytest.raises(IntegrityError): 
            obj1.delete()

    def test_return_product_line_active_only_true(self, product_line_factory):
        """Testing IsActiveQueryset ... object"""
        product_line_factory(is_active=True) 
        product_line_factory(is_active=False) #This first 2 lines creates two new product lines
        qs = ProductLine.objects.is_active().count()
        assert qs == 1

    def test_return_product_line(self, product_line_factory):
        """Testing Normal behaviour"""
        product_line_factory(is_active=True) 
        product_line_factory(is_active=False) #This first 2 linew creates two new product lines
        qs = ProductLine.objects.count()
        assert qs == 2

class TestProductImageModel:
    """This factory will initiate/start all the other factories it is connected to"""
    def test_str_method(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku="12345")
        obj2 = product_image_factory(order=1, product_line=obj1) #product_line__sku="12345" # Table Traversing
        assert obj2.__str__() == "12345_img" # "1"

    def test_duplicate_order_values(self, product_image_factory, product_line_factory):
        obj = product_line_factory() 
        product_image_factory(order=1, product_line=obj) #creating a product line using that product #Fk

        with pytest.raises(ValidationError):
            # same as the line above, and calling the clean() method in addition
            product_image_factory(order=1, product_line=obj).clean()


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        attr = attribute_factory(name="test") #M2M many-to-many
        obj = product_type_factory.create(name="test_type", attribute=(attr, ))
        # x = ProductTypeAttribute.objects.filter(id=1)
        # print(x)
        assert obj.__str__() == "test_type"

    def test_name_max_length(self, product_type_factory):
        name = "x" * 101
        obj = product_type_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(name="test_attribute")
        assert obj.__str__() == "test_attribute"

    def test_name_max_length(self, attribute_factory):
        name = "x" * 101  #"xxxxxxxxxxxxxxxxxxxxxxxx"
        obj = attribute_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()


class TestAttributeValueModel:
    """Because of the string output concatenates 2 things, quite different from the rest, but Not a Many-to_many"""
    def test_str_method(self, attribute_value_factory, attribute_factory):
        obj_a = attribute_factory(name="test_attribute") #output has 2 things obj_a and obj_b
        obj_b = attribute_value_factory.create(attribute_value="test_value", attribute=obj_a)
        assert obj_b.__str__() == "test_attribute-test_value"

    def test_name_max_length(self, attribute_value_factory):
        attribute_value = "x" * 101  
        obj = attribute_value_factory(attribute_value=attribute_value)
        with pytest.raises(ValidationError):
            obj.full_clean()



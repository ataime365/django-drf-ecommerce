import pytest
import json

pytestmark = pytest.mark.django_db #Available globally, no need to design each funtion,

class TestCategoryEndpoints:

    endpoint = "/api/category/"

    def test_category_get(self, category_factory, api_client): #Testing the get request endpoint for category
        # Arrange
        # category_factory() #This line automatically adds data to the database
        category_factory.create_batch(4) # creates 4 new entries in the db
        #Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        print(json.loads(response.content))
        assert len(json.loads(response.content)) == 4


class TestBrandEndpoints:

    endpoint = "/api/brand/"

    def test_brand_get(self, brand_factory, api_client): #Testing the get request endpoint for category
        # Arrange
        # brand_factory() #This line automatically adds data to the database
        brand_factory.create_batch(4) # creates 4 new entries in the db
        #Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoints:

    endpoint = "/api/product/"
    def test_product_get(self, product_factory, api_client): #Testing the get request endpoint for category
        # Arrange
        # product_factory() #This line automatically adds data to the database
        product_factory.create_batch(4) # creates 4 new entries in the db
        #Act
        response = api_client().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4



        
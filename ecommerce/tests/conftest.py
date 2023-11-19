# The conftest file is read first, before the tests starts
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import CategoryFactory, BrandFactory, ProductFactory

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)

# category_factory #This is how CategoryFactory must be assesed, lower case, with an underscore
# category_factory is now available globally

@pytest.fixture
def api_client():
    return APIClient




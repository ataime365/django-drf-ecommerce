from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection

# from pygments import highlight # Not necessary
# from pygments.formatters import TerminalFormatter
# from pygments.lexers.sql import SqlLexer #depends on the database you are using #PostgresLexer for Postgres db
# from sqlparse import format

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


class CategoryView(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(responses=CategorySerializer, tags=['category']) #Docs
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    

class BrandView(viewsets.ViewSet):
    """
    A simple Viewset for viewing all brands
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @extend_schema(responses=BrandSerializer, tags=['brand']) #Docs
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
    

@extend_schema(responses=ProductSerializer, tags=['product']) #Docs
class ProductView(viewsets.ViewSet):
    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.all().isactive() #Product.objects.all() #Product.isactive.all() 
    serializer_class = ProductSerializer

    lookup_field = "slug"

    def retrieve(self, request, slug=None): #default lookup field is pk i.e  pk=None
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related("category", "brand") , 
            many=True) #many=True to avoid errors #slug field isnt unique yet #select_related does all the table joins for us
        data = Response(serializer.data)

        # Not so Neccessary
        # q = list(connection.queries)
        # print(len(q)) #Amiunt of queries
        # for qs in q:
        #     sqlformatted = format(str(qs['sql']), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        return data
    
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=["get"], 
            detail=False, 
            url_path=r"category/(?P<category>\w+)/all",) #when our url_path is dynamic
    def list_product_by_category(self, request, category=None):
        """
        An endpoint to return product by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__name=category), many=True) #category__name => Traversing between tables
        return Response(serializer.data)





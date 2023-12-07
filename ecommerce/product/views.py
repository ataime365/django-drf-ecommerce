from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django.db import connection

from pygments import highlight # Not necessary
from pygments.formatters import TerminalFormatter
from pygments.lexers.sql import SqlLexer #depends on the database you are using #PostgresLexer for Postgres db
from sqlparse import format

from .models import Category, Product, ProductLineAttributeValue, ProductLine, ProductImage #ProductLine, ProductImage used for ordering and filtering
from .serializers import CategorySerializer, ProductSerializer, ProductCategorySerializer


class CategoryView(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all().is_active()
    serializer_class = CategorySerializer

    @extend_schema(responses=CategorySerializer, tags=['category']) #Docs
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    

@extend_schema(responses=ProductSerializer, tags=['product']) #Docs
class ProductView(viewsets.ViewSet):
    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.all().is_active() #Product.objects.all() #Product.isactive.all() 
    serializer_class = ProductSerializer

    lookup_field = "slug"

    def retrieve(self, request, slug=None): #default lookup field is pk i.e  pk=None
        """
        An endpoint to return a product by name
        """
        serializer = ProductSerializer( #self.queryset.filter()
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch("attribute_value__attribute")) #For performance
            .prefetch_related(Prefetch("product_line__product_image")) #For performance
            .prefetch_related(Prefetch("product_line__attribute_value__attribute")) #For performance
            ,
              #traversing(joining) 3 tables using their related_name  #Prefetch(related_name1)
            many=True) #many=True to avoid errors #slug field isnt unique yet #select_related does all the table joins for us
        data = Response(serializer.data)

        # Not so Neccessary
        # q = list(connection.queries)
        # print(len(q)) #Amount of queries
        # for qs in q:
        #     sqlformatted = format(str(qs['sql']), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        return data
    

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    

    @action(methods=["get"], detail=False, 
            url_path=r"category/(?P<slug>[\w-]+)",) #when our url_path is dynamic
    def list_product_by_category_slug(self, request, slug=None): #category=None @category name is changed to category slug
        """
        An endpoint to return products by category
        """
        # serializer = ProductSerializer(self.queryset.filter(category__slug=slug), many=True) #category__name => Traversing between tables
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(Prefetch("product_line", queryset=ProductLine.objects.order_by("order"))) 
            .prefetch_related(Prefetch("product_line__product_image", queryset=ProductImage.objects.filter(order=1))) #.order_by("order"))) , This can also work, Serializer will change a bit image = first_product_line["product_image"][0]
            , #The queryset inside, extends the queryset outside
            many=True) 
        #category__name => Traversing between tables

        data = Response(serializer.data)
        return data





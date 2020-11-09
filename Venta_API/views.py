from django.shortcuts import render
from rest_framework import viewsets
from .models import Client, Article, Sale
from .serializers import ClientSerializer, ArticleSerializer, SaleSerializer

# Reescribir las vistas con la librería de django-rest-framework, ejemplo con ViewSets

class ClientViewSet(viewsets.ModelViewSet):
    """
    Vista del modelo Client
    """
    model = Client
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Vista del modelo Article
    """
    model = Article
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class SaleViewSet(viewsets.ModelViewSet):
    """
    Vista del modelo Sale
    """
    model = Sale
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
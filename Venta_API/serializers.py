from rest_framework import serializers
from .models import Client, Article, Sale

"""
Para cada una de los objetos crear un serializer, para las tablas de Articulos y
Clientes crear un serializer que dependa de Serializer y para la tabla de Ventas un
ModelSerializer
"""

class ClientSerializer(serializers.Serializer):
    """
    Serializador del modelo Client
    """
    id = serializers.IntegerField(read_only=True)

    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    dni = serializers.CharField(max_length=8)
    email = serializers.EmailField()

    created = serializers.DateTimeField(read_only=True)
    edited = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Client.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.dni = validated_data.get('dni', instance.dni)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
class ArticleSerializer(serializers.Serializer):
    """
    Serializador del modelo Article
    """
    id = serializers.IntegerField(read_only=True)

    description = serializers.CharField(max_length=50)
    code = serializers.CharField(max_length=50)
    price = serializers.FloatField()

    created = serializers.DateTimeField(read_only=True)
    edited = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Article.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.description = validated_data.get('description', instance.description)
        instance.code = validated_data.get('code', instance.code)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class SaleSerializer(serializers.ModelSerializer):
    """
    Serializador del modelo Sale
    """
    #articles = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), many=True, read_only=False)
    total = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Sale
        depth = 1 #Profundidad de la consulta, trae datos del cliente
        fields = '__all__' #O lista con campos específicos, en caso de no querer todos los campos
    
    def create(self, validated_data):
        """
        POST SaleSerializer
        Obtener precios de los articulos seleccionados para calcular el total.
        Al ser 'articles' del tipo 'ManyToManyField', primero se debe crear el objeto Sale sin las relaciones, y luego setearlas con set.
        """
        #Calculo del monto de acuerdo a los articulos
        price_s = 0
        for i in validated_data['articles']:
            price_s += Article.objects.filter(id=i.id).first().price

        articles = validated_data.pop('articles')

        sale = Sale.objects.create(**validated_data)
        sale.articles.set(articles)
        sale.total = price_s
        sale.save()
        return sale
    
    def update(self, instance, validated_data):
        """
        PUT SaleSerializer
        Al ser 'articles' del tipo 'ManyToManyField', el campo se establece con set.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.articles.set(validated_data.get('articles', instance.articles))
        instance.client = validated_data.get('client', instance.client)

        #Calculo del monto de acuerdo a los articulos
        price_s = 0
        for i in validated_data['articles']:
            price_s += Article.objects.filter(id=i.id).first().price

        instance.total = price_s
        instance.save()
        return instance


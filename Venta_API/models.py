from django.db import models

# Create your models here.
class Client(models.Model):
    """
    Modelo de los clientes.
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dni = models.CharField(max_length=8)
    email = models.EmailField()

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Article(models.Model):
    description = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    price = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} = {}'.format(self.code, self.description, self.price)


class Sale(models.Model):

    client = models.ForeignKey(Client, null=False, blank=False, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)
    total = models.FloatField(null=True) #Primero guardo el objeto para poder usar las relaciones, una vez obtenido el monto total se actualiza

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

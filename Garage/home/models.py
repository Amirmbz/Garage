from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.PositiveBigIntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

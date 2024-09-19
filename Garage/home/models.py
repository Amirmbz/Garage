from django.db import models


# Create your models here.
class product(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    price = models.PositiveBigIntegerField()
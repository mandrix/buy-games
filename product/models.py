from django.db import models

# Create your models here.

from django.db import models
from enum import Enum


class ConsoleEnum(Enum):
    PlayStation1 = "ps1"
    PlayStation2 = "ps2"
    PlayStation3 = "ps3"
    PlayStation4 = "ps4"
    PlayStation5 = "ps5"


class Product(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    barcode = models.CharField(max_length=100, unique=True)
    creation_date = models.DateField(auto_now_add=True)
    modification_date = models.DateField(auto_now=True)
    departure_date = models.DateField()

    def __str__(self):
        return self.price


class Console(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    console = models.CharField(
        max_length=20,
        choices=[(console.value, console.name) for console in ConsoleEnum]
    )

    def __str__(self):
        return self.console


class VideoGame(models.Model):
    title = models.CharField(max_length=100)
    console = models.CharField(
        max_length=20,
        choices=[(console.value, console.name) for console in ConsoleEnum]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #genero = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Collectable(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.description

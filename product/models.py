from django.db import models

# Create your models here.

from django.db import models


class RegionEnum(models.TextChoices):
    Japan = "jp", "Japan"
    USA = "usa", "USA"
    Europe = "eu", "Europe"


class OwnerEnum(models.TextChoices):
    Joseph = "joseph", "Joseph"
    Mauricio = "mauricio", "Mauricio"
    Business = "business", "Business"


class ConsoleEnum(models.TextChoices):
    PlayStation1 = "ps1", "PS1"
    PlayStation2 = "ps2", "PS2"
    PlayStation3 = "ps3", "PS3"
    PlayStation4 = "ps4", "PS4"
    PlayStation5 = "ps5", "PS5"
    N64 = "n64", "N64"
    Snes = "snes", "SNES"
    Switch = "switch", "Nintendo Switch"


class Product(models.Model):
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    provider_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="En colones")
    barcode = models.CharField(max_length=100, unique=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    provider_purchase_date = models.DateField()
    sale_date = models.DateField(null=True)
    owner = models.CharField(max_length=100, choices=OwnerEnum.choices, null=True)
    description = models.TextField(default="")
    region = models.CharField(max_length=100, choices=RegionEnum.choices, null=True)


class Console(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )

    def __str__(self):
        return self.console


class VideoGame(models.Model):
    title = models.CharField(max_length=100, default="")
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Collectable(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Accessory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    console = models.CharField(
        max_length=20,
        choices=ConsoleEnum.choices,
        null=True
    )

    def __str__(self):
        return self.title

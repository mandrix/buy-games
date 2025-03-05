from django.db import models

import product.models


class FoodEnum(models.TextChoices):
    main_dish = "mainDish", "Plato Principal"

class Food(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=FoodEnum.choices, default=FoodEnum.main_dish.value)

    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.product.type = product.models.ProductTypeEnum.food
        self.product.save()
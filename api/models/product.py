# models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    duty_rate = models.DecimalField(max_digits=5, decimal_places=2) 

    def __str__(self):
        return self.name


# Pour enregistrer les marchandises simulables
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
     # en pourcentage

    def __str__(self):
        return f"{self.name} ({self.category.duty_rate}%)"

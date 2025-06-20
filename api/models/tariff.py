# models.py

from django.db import models

# Pour classer les marchandises
class TariffCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    duty_rate = models.DecimalField(max_digits=5, decimal_places=2)  # en pourcentage

    def __str__(self):
        return f"{self.name} ({self.duty_rate}%)"

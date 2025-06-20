# models.py

from django.db import models
from .simulationrequest import SimulationRequest
# Paiement lié à une simulation
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('orange', 'Orange Money'),
        ('mtn', 'MTN Mobile Money'),
    ]
    simulation = models.OneToOneField(SimulationRequest, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    confirmed = models.BooleanField(default=False)
    payment_code = models.CharField(max_length=50)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement #{self.id} - {self.simulation}"

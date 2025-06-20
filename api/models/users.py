# models.py

from django.db import models


# Pour les utilisateurs effectuant la simulation
class UserInfo(models.Model):
    LEGAL_STATUS_CHOICES = [
        ('physique', 'Personne physique'),
        ('morale', 'Personne morale'),
    ]
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    legal_status = models.CharField(max_length=10, choices=LEGAL_STATUS_CHOICES)

    def __str__(self):
        return self.full_name

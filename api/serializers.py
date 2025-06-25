from .models import (Product, Category, ImportSimulation, DutiesBreakdown)
from rest_framework import serializers

"""
Sérialiseur pour le modèle Product.
Sérialise tous les champs de l'instance Product.
"""
"""
Sérialiseur pour le modèle Category.
Sérialise tous les champs de l'instance Category.
"""
"""
Sérialiseur pour le modèle ImportSimulation.
Sérialise tous les champs de l'instance ImportSimulation.
"""
"""
Sérialiseur pour le modèle DutiesBreakdown.
Sérialise tous les champs de l'instance DutiesBreakdown.
"""

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"        
        
class ImportSimulationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImportSimulation
        fields = "__all__"        
        
class DutiesBreakdownSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DutiesBreakdown
        fields = "__all__"                
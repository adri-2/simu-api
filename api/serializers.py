from .models import ( Product,Category,ImportSimulation,DutiesBreakdown)
from rest_framework import serializers

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
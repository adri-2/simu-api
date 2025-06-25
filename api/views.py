from django.shortcuts import render
"""
This module defines API views for managing products, categories, import simulations, and duties breakdowns.
Classes:
    ProductViewset(ReadOnlyModelViewSet):
        Viewset for listing and retrieving products. Accessible only by admin users.
    AdminProductViewset(ModelViewSet):
        Viewset for full CRUD operations on products. Accessible only by admin users.
    CategoryViewset(ReadOnlyModelViewSet):
        Viewset for listing and retrieving categories. Accessible by authenticated users.
    AdminCategoryViewset(ModelViewSet):
        Viewset for full CRUD operations on categories. Accessible only by admin users.
    ImportSimulationViewset(ModelViewSet):
        Viewset for managing import simulations. Accessible only by the owner of the simulation.
    DutiesBreakdownViewset(ModelViewSet):
        Viewset for managing duties breakdowns. Accessible by authenticated users and filtered by user.
    ProductCategoryView(APIView):
        API view to retrieve the category of a specific product by its primary key. Accessible by authenticated users.
"""
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import ( Product,ImportSimulation,Category,DutiesBreakdown)
from .serializers import ProductSerializer,CategorySerializer,ImportSimulationSerializer,DutiesBreakdownSerializer
# Create your views here.
from .permissions import IsAdminAuthenticated, IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductViewset(ReadOnlyModelViewSet):
    
    serializer_class = ProductSerializer
   
    queryset = Product.objects.all()
    permission_classes = [IsAdminAuthenticated]
    

class AdminProductViewset(ModelViewSet):
    
    serializer_class = ProductSerializer
    # pagination_class = '10'
    permission_classes = [IsAdminAuthenticated]
    # def get_queryset(self):
    queryset = Product.objects.all()        

    
class CategoryViewset(ReadOnlyModelViewSet):
    
    serializer_class = CategorySerializer

    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

class AdminCategoryViewset(ModelViewSet):
    
    serializer_class = CategorySerializer
    
    permission_classes = [IsAdminAuthenticated]
    # def get_queryset(self):
    queryset = Category.objects.all()    
    
class ImportSimulationViewset(ModelViewSet):
    
    serializer_class = ImportSimulationSerializer
    
    permission_classes = [IsOwner]
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ImportSimulation.objects.none()
            
        return ImportSimulation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
class DutiesBreakdownViewset(ModelViewSet):
    
    serializer_class = DutiesBreakdownSerializer
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DutiesBreakdown.objects.filter(user=self.request.user)

class ProductCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            category = product.category
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Produit non trouvé.'}, status=404)



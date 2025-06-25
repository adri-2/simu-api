from rest_framework import routers
"""
Ce fichier définit les routes de l'API pour l'application Django en utilisant le framework Django REST Framework.
Il configure les routes principales pour les ressources suivantes :
- Produits (products)
- Catégories (categories)
- Simulations d'importation (simulations)
- Détail des droits de douane (dutiesbreakdown)
- Gestion administrateur des produits et catégories (admin/products, admin/categories)
Les routes sont enregistrées à l'aide d'un SimpleRouter, ce qui permet de générer automatiquement les endpoints RESTful pour chaque ViewSet associé.
En plus des routes générées par le routeur, ce fichier définit également :
- Un endpoint pour l'authentification JWT (login) permettant d'obtenir un token d'accès et de rafraîchissement.
- Un endpoint pour rafraîchir le token JWT.
- Un endpoint pour obtenir la catégorie associée à un produit spécifique.
Ce fichier centralise donc la configuration des URLs pour l'ensemble des fonctionnalités exposées par l'API.
"""
from .views import( ProductViewset,CategoryViewset,ImportSimulationViewset,DutiesBreakdownViewset,
                   AdminCategoryViewset,AdminProductViewset,ProductCategoryView)
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = routers.SimpleRouter()
# Aucun code supplémentaire requis ici pour le moment
router.register('products',ProductViewset,basename='products')
router.register('categories',CategoryViewset,basename='categories')
router.register('admin/products',AdminProductViewset,basename='admin-products')
router.register('admin/categories',AdminCategoryViewset,basename='admin-categories')
router.register('simulations',ImportSimulationViewset,basename='simulations')
router.register('dutiesbreakdown',DutiesBreakdownViewset,basename='dutiesbreakdown')

urlpatterns = [
     path('', include(router.urls)), 
     path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('product/<int:pk>/category/', ProductCategoryView.as_view(), name='product-category'),
]
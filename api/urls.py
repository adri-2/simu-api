# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



from .views import (
     UserRegistrationView, UserProfileView,
    ProductCategoryViewSet, ProductViewSet, SimulationViewSet,SimulationViewSetHistorique
)

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'simulations', SimulationViewSet)
# router.register(r'simulations/historique/', SimulationViewSet, basename='simulation-historique')
router.register(r'historique_simulations', SimulationViewSetHistorique, basename='simulation-historique')






urlpatterns = [
    # Authentification JWT
      path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/register/', UserRegistrationView.as_view(), name='user_register'),

    # Profil utilisateur
    # path('simulations/historique/', SimulationViewSetHistorique, name='simulation-historique'),
      path('profile/', UserProfileView.as_view(), name='user-profile'),

    # API resources avec ViewSets et Routers
    path('', include(router.urls)),
    
    
    
  
]



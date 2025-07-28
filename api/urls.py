# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
#      TokenObtainPairView,
#     TokenVerifyView,
# )




from .views import (
    CustomTokenObtainPairView, UserRegistrationView, UserProfileView,
    ProductCategoryViewSet, ProductViewSet, SimulationViewSet
)

router = DefaultRouter()
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'simulations', SimulationViewSet)

urlpatterns = [
    # Authentification JWT
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', UserRegistrationView.as_view(), name='user_register'),

    # Profil utilisateur
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # API resources avec ViewSets et Routers
    path('', include(router.urls)),
    
    
    
  
]



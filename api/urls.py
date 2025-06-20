from rest_framework import routers
from .views import( ProductViewset,CategoryViewset,ImportSimulationViewset,DutiesBreakdownViewset,
                   AdminCategoryViewset,AdminProductViewset)
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = routers.SimpleRouter()

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
]
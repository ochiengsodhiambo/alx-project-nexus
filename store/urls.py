from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    CategoryViewSet,
    RegisterAPIView,
    CartView,
    OrderView,
    SellerViewSet,
)

# Router for Product and Category ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sellers', SellerViewSet) 


urlpatterns = [
    path('', include(router.urls)),  # router URLs
    path('auth/register/', RegisterAPIView.as_view(), name='register'), # User registration endpoint
    path('cart/', CartView.as_view(), name='cart'),     # Cart endpoints
    path('orders/', OrderView.as_view(), name='orders'),    # Order endpoints
]



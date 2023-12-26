from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkObjectViewSet, ProductViewSet, FactoryViewSet, RetailNetworkViewSet, EntrepreneurViewSet, SupplierViewSet, api_index


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'network-objects', NetworkObjectViewSet, basename='network-objects')
router.register(r'factories', FactoryViewSet, basename='factories')
router.register(r'retail-networks', RetailNetworkViewSet, basename='retail-networks')
router.register(r'entrepreneurs', EntrepreneurViewSet, basename='entrepreneurs')

urlpatterns = [
    path('api/index/', api_index, name='api_index'),
    path('', api_index, name='api_index'),
    path('api/', include(router.urls)),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]

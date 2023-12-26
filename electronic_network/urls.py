from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""
Основные URL-маршруты
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('electronics.urls')),
    path('electronics/', include('electronics.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
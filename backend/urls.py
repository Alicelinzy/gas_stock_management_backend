from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gas_management.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/v1/logout/', TokenObtainPairView.as_view(), name='logout'),
    path('api-auth/', include('rest_framework.urls')),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'inventory', views.GasInventoryViewSet, basename='gas-inventory')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'ratings', views.RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    # API v1 routes compatible with README documentation
    path('v1/register/', views.RegisterView.as_view(), name='v1-register'),
    path('v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('v1/gas/', views.GasInventoryViewSet.as_view({'get': 'list'}), name='v1-gas-list'),
    path('v1/orders/', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='v1-orders'),
    path('v1/feedback/', views.RatingViewSet.as_view({'post': 'create'}), name='v1-feedback'),
    path('v1/seller/inventory/', views.GasInventoryViewSet.as_view({'get': 'my_inventory', 'post': 'create'}), name='v1-seller-inventory'),
    path('v1/seller/orders/', views.OrderViewSet.as_view({'get': 'seller_orders'}), name='v1-seller-orders'),
    path('v1/seller/invoice/', views.InvoiceViewSet.as_view({'post': 'create'}), name='v1-seller-invoice'),
    path('v1/admin/orders/pending/', views.OrderViewSet.as_view({'get': 'list'}), {'status': 'PENDING'}, name='v1-admin-orders-pending'),
    path('v1/admin/invoices/pending/', views.InvoiceViewSet.as_view({'get': 'list'}), {'admin_approval': False}, name='v1-admin-invoices-pending'),
    
    # Adding explicit endpoints for actions
    path('orders/<int:pk>/approve/', views.OrderViewSet.as_view({'post': 'approve'}), name='order-approve'),
    path('orders/<int:pk>/reject/', views.OrderViewSet.as_view({'post': 'reject'}), name='order-reject'),
    path('orders/<int:pk>/cancel/', views.OrderViewSet.as_view({'post': 'cancel'}), name='order-cancel'),
    path('orders/<int:pk>/mark-delivered/', views.OrderViewSet.as_view({'post': 'mark_delivered'}), name='order-mark-delivered'),
    path('invoices/<int:pk>/approve/', views.InvoiceViewSet.as_view({'post': 'approve'}), name='invoice-approve'),
    path('invoices/<int:pk>/mark-as-paid/', views.InvoiceViewSet.as_view({'post': 'mark_as_paid'}), name='invoice-mark-as-paid'),
]

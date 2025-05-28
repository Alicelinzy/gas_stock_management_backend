from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import UserProfile, GasInventory, Order, Invoice, Payment, Rating
from .serializers import (
    UserSerializer, UserProfileSerializer, GasInventorySerializer,
    OrderSerializer, InvoiceSerializer, PaymentSerializer, RatingSerializer,
    UserRegistrationSerializer
)
from .permissions import IsBuyer, IsSeller, IsAdmin, IsSellerOrReadOnly, IsBuyerOrSellerOrAdmin

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

class GasInventoryViewSet(viewsets.ModelViewSet):
    queryset = GasInventory.objects.all()
    serializer_class = GasInventorySerializer
    permission_classes = [permissions.IsAuthenticated, IsSellerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand', 'location']
    ordering_fields = ['unit_price', 'weight_kg', 'date_added']
    
    def get_queryset(self):
        queryset = GasInventory.objects.all()
        
        # Filter by brand
        brand = self.request.query_params.get('brand', None)
        if brand:
            queryset = queryset.filter(brand__iexact=brand)
            
        # Filter by weight
        weight = self.request.query_params.get('weight', None)
        if weight:
            # Remove 'kg' suffix if present and convert to decimal
            try:
                if 'kg' in weight.lower():
                    weight = weight.lower().replace('kg', '').strip()
                weight_value = float(weight)
                queryset = queryset.filter(weight_kg=weight_value)
            except ValueError:
                pass
            
        # Filter by location
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(unit_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(unit_price__lte=max_price)
            
        # Filter by seller
        seller_id = self.request.query_params.get('seller', None)
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)
            
        # Only show inventory with quantity > 0
        queryset = queryset.filter(quantity__gt=0)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_inventory(self, request):
        queryset = self.get_queryset().filter(seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyerOrSellerOrAdmin]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'status']
    
    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)
        
        # Admins can see all orders
        if profile.role == 'ADMIN':
            return Order.objects.all()
            
        # Regular users can see orders where they're the buyer or the seller
        return Order.objects.filter(
            Q(buyer=user) | Q(gas_inventory__seller=user)
        )
    
    def create(self, request, *args, **kwargs):
        # Check if user is a buyer
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.role != 'BUYER':
            return Response(
                {"detail": "Only buyers can place orders."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Check if quantity is available
        gas_inventory_id = request.data.get('gas_inventory')
        quantity = int(request.data.get('quantity', 0))
        
        try:
            gas_inventory = GasInventory.objects.get(pk=gas_inventory_id)
            if quantity <= 0:
                return Response(
                    {"detail": "Quantity must be greater than 0."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if quantity > gas_inventory.quantity:
                return Response(
                    {"detail": "Not enough inventory available."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except GasInventory.DoesNotExist:
            return Response(
                {"detail": "Gas inventory not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        queryset = Order.objects.filter(buyer=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def seller_orders(self, request):
        queryset = Order.objects.filter(gas_inventory__seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        order = self.get_object()
        
        # Check if user is admin
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.role != 'ADMIN':
            return Response(
                {"detail": "Only admins can approve orders."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if order.status != 'PENDING':
            return Response(
                {"detail": f"Cannot approve order with status {order.status}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if there's enough inventory
        if order.quantity > order.gas_inventory.quantity:
            return Response(
                {"detail": "Not enough inventory to fulfill this order."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Update order status
        order.status = 'APPROVED'
        order.save()
        
        # Decrease inventory quantity
        inventory = order.gas_inventory
        inventory.quantity -= order.quantity
        inventory.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        order = self.get_object()
        
        # Check if user is admin
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.role != 'ADMIN':
            return Response(
                {"detail": "Only admins can reject orders."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if order.status != 'PENDING':
            return Response(
                {"detail": f"Cannot reject order with status {order.status}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        order.status = 'REJECTED'
        order.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        # Only the buyer can cancel their order
        if request.user != order.buyer:
            return Response(
                {"detail": "You do not have permission to cancel this order."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if order.status not in ['PENDING', 'APPROVED']:
            return Response(
                {"detail": f"Cannot cancel order with status {order.status}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If order was approved, return quantity to inventory
        if order.status == 'APPROVED':
            inventory = order.gas_inventory
            inventory.quantity += order.quantity
            inventory.save()
            
        order.status = 'CANCELLED'
        order.save()
        
        return Response(OrderSerializer(order).data)
        
    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        order = self.get_object()
        
        # Check if user is seller of this order
        if request.user != order.gas_inventory.seller and not request.user.is_staff:
            return Response(
                {"detail": "Only the seller or admin can mark orders as delivered."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if order.status != 'APPROVED':
            return Response(
                {"detail": f"Cannot mark as delivered an order with status {order.status}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        order.status = 'DELIVERED'
        order.save()
        
        return Response(OrderSerializer(order).data)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)
        
        # Admins can see all invoices
        if profile.role == 'ADMIN':
            return Invoice.objects.all()
            
        # Regular users can see invoices for orders where they're the buyer or seller
        return Invoice.objects.filter(
            Q(order__buyer=user) | Q(order__gas_inventory__seller=user)
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        invoice = self.get_object()
        
        # Check if user is admin
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.role != 'ADMIN':
            return Response(
                {"detail": "Only admins can approve invoices."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if invoice.admin_approval:
            return Response(
                {"detail": "Invoice already approved."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if the associated order is approved
        if invoice.order.status != 'APPROVED':
            return Response(
                {"detail": "Cannot approve invoice for an order that is not approved."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        invoice.admin_approval = True
        invoice.admin_approval_date = timezone.now()
        invoice.save()
        
        return Response(InvoiceSerializer(invoice).data)
        
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        invoice = self.get_object()
        
        # Only admin can mark as paid
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.role != 'ADMIN':
            return Response(
                {"detail": "Only admins can mark invoices as paid."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if invoice.is_paid:
            return Response(
                {"detail": "Invoice already marked as paid."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        invoice.is_paid = True
        invoice.payment_date = timezone.now()
        invoice.save()
        
        # Optionally create payment record
        Payment.objects.create(
            invoice=invoice,
            amount=invoice.order.total_price,
            status='COMPLETED',
            payment_method='Admin Approved'
        )
        
        return Response(InvoiceSerializer(invoice).data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)
        
        # Admins can see all payments
        if profile.role == 'ADMIN':
            return Payment.objects.all()
            
        # Regular users can see payments for their orders
        return Payment.objects.filter(
            Q(invoice__order__buyer=user) | Q(invoice__order__gas_inventory__seller=user)
        )

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)
        
        # Admins can see all ratings
        if profile.role == 'ADMIN':
            return Rating.objects.all()
            
        # Regular users can see ratings for their orders (as buyer)
        # or ratings for orders related to their inventory (as seller)
        return Rating.objects.filter(
            Q(order__buyer=user) | Q(order__gas_inventory__seller=user)
        )
    
    def create(self, request, *args, **kwargs):
        # Check if the user is the buyer of the order
        order_id = request.data.get('order')
        try:
            order = Order.objects.get(pk=order_id)
            if order.buyer != request.user:
                return Response(
                    {"detail": "You can only rate orders you've purchased."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Check if the order status is DELIVERED
            if order.status != 'DELIVERED':
                return Response(
                    {"detail": "You can only rate orders that have been delivered."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Check if a rating already exists
            if Rating.objects.filter(order=order).exists():
                return Response(
                    {"detail": "You have already rated this order."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        return super().create(request, *args, **kwargs)
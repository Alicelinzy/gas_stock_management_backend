from rest_framework import permissions
from .models import UserProfile

class IsBuyer(permissions.BasePermission):
    """
    Custom permission to only allow buyers to create orders.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'BUYER'
        except UserProfile.DoesNotExist:
            return False

class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow sellers to create and manage inventory.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'SELLER'
        except UserProfile.DoesNotExist:
            return False

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to approve orders and invoices.
    """
    def has_permission(self, request, view):
        try:
            profile = UserProfile.objects.get(user=request.user)
            return profile.role == 'ADMIN'
        except UserProfile.DoesNotExist:
            return False

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sellers to edit their own inventory.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the seller
        return obj.seller == request.user

class IsBuyerOrSellerOrAdmin(permissions.BasePermission):
    """
    Permission to allow only the buyer, seller, or admin to access the order.
    """
    def has_object_permission(self, request, view, obj):
        try:
            profile = UserProfile.objects.get(user=request.user)
            
            # Admin can access anything
            if profile.role == 'ADMIN':
                return True
                
            # Buyer can access their own orders
            if obj.buyer == request.user:
                return True
                
            # Seller can access orders for their inventory
            if obj.gas_inventory.seller == request.user:
                return True
                
            return False
        except UserProfile.DoesNotExist:
            return False
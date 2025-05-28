from django.contrib import admin
from .models import UserProfile, GasInventory, Order, Invoice, Payment, Rating

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Django admin configuration for UserProfile model.
    This admin class provides a customized interface for managing UserProfile instances
    in the Django admin panel.
    Attributes:
        list_display (tuple): Fields to display in the admin list view.
            Shows user, role, and phone_number columns.
        list_filter (tuple): Fields to filter by in the admin interface.
            Allows filtering by role.
        search_fields (tuple): Fields to search through in the admin search bar.
            Enables searching by username, email, and phone_number.
    """

    list_display = ('user', 'role', 'phone_number')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(GasInventory)
class GasInventoryAdmin(admin.ModelAdmin):
    """Django admin configuration for GasInventory model."""
    
    list_display = ('brand', 'weight_kg', 'quantity', 'unit_price', 'seller', 'location', 'date_added')
    list_filter = ('brand', 'weight_kg', 'location')
    search_fields = ('brand', 'seller__username', 'location')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Django admin configuration for Order model."""
    list_display = ('id', 'buyer', 'gas_inventory', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'id', 'delivery_address')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Invoice model.

    Provides a customized admin interface for managing invoices with enhanced
    list display, filtering, and search capabilities.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view including
            invoice number, associated order, payment status, admin approval status,
            payment date, and creation timestamp.
        list_filter (tuple): Filter options for the admin list view allowing
            filtering by payment status, admin approval, and creation date.
        search_fields (tuple): Searchable fields enabling search by invoice number
            and the username of the order's buyer.
    """
    list_display = ('invoice_number', 'order', 'is_paid', 'admin_approval', 'payment_date', 'created_at')
    list_filter = ('is_paid', 'admin_approval', 'created_at')
    search_fields = ('invoice_number', 'order__buyer__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Django admin configuration for Payment model.

    This admin class provides a comprehensive interface for managing payment records
    in the Django admin panel.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view including
            invoice, amount, status, payment method, and creation timestamp.
        list_filter (tuple): Filter options in the admin sidebar for status,
            payment method, and creation date.
        search_fields (tuple): Searchable fields including transaction ID and
            invoice number for quick payment lookup.
    """
    """"""
    list_display = ('invoice', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'invoice__invoice_number')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Django admin configuration for Rating model."""
    
    list_display = ('order', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

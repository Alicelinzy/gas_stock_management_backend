from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    """ User Profile model to extend the default User model with additional fields."""
    USER_ROLES = [
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
        ('ADMIN', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=USER_ROLES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} ({self.role})'

class GasInventory(models.Model):
    """ Model to manage gas inventory for different brands and weights."""
    GAS_BRAND_CHOICES = [
        ('JIBU', 'Jibu'),
        ('MERU', 'Meru'),
        ('TOTAL', 'Total'),
        ('OTHER', 'Other'),
    ]
    
    brand = models.CharField(max_length=20, choices=GAS_BRAND_CHOICES)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, help_text='Weight in kilograms')
    quantity = models.PositiveIntegerField(help_text='Number of bottles/units available')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gas_inventory')
    location = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.brand} - {self.weight_kg}kg ({self.quantity} units) at {self.location}'
    
    class Meta:
        verbose_name_plural = 'Gas Inventories'
        ordering = ['-date_added']

class Order(models.Model):
    """ Model to manage orders placed by buyers for gas inventory."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    gas_inventory = models.ForeignKey(GasInventory, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    delivery_address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order #{self.id} - {self.gas_inventory.brand} ({self.status})'
    
    class Meta:
        ordering = ['-created_at']

class Invoice(models.Model):
    """ Model to manage invoices generated for orders."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    admin_approval = models.BooleanField(default=False)
    admin_approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate a unique invoice number when first created
            self.invoice_number = f'INV-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Invoice #{self.invoice_number} - {self.order.gas_inventory.brand}'

class Payment(models.Model):
    """ Model to manage payments made for invoices."""
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Payment of {self.amount} for Invoice #{self.invoice.invoice_number}'

class Rating(models.Model):
    """ Model to manage ratings and feedback for orders."""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Rating: {self.rating}/5 for Order #{self.order.id}'

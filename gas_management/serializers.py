from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, GasInventory, Order, Invoice, Payment, Rating

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User model to include basic user information. """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer for UserProfile model to include user role and contact details. """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'phone_number', 'address']

class GasInventorySerializer(serializers.ModelSerializer):
    """ Serializer for GasInventory model to manage gas inventory details. """
    seller_name = serializers.ReadOnlyField(source='seller.username')
    
    class Meta:
        model = GasInventory
        fields = ['id', 'brand', 'weight_kg', 'quantity', 'unit_price', 
                 'seller', 'seller_name', 'location', 'date_added', 'last_updated']
        read_only_fields = ['seller']
    
    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model to manage orders placed by buyers. """
    buyer_name = serializers.ReadOnlyField(source='buyer.username')
    seller_name = serializers.ReadOnlyField(source='gas_inventory.seller.username')
    gas_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'gas_inventory', 'gas_details', 'buyer', 'buyer_name', 
                 'seller_name', 'quantity', 'total_price', 'status',
                 'delivery_address', 'contact_phone', 'created_at', 'updated_at']
        read_only_fields = ['buyer', 'total_price', 'status']
    
    def get_gas_details(self, obj):
        return {
            'brand': obj.gas_inventory.brand,
            'weight_kg': obj.gas_inventory.weight_kg,
            'unit_price': obj.gas_inventory.unit_price,
            'location': obj.gas_inventory.location,
        }
    
    def create(self, validated_data):
        # Set buyer to current user
        validated_data['buyer'] = self.context['request'].user
        
        # Calculate total price based on gas inventory unit price and quantity
        gas_inventory = validated_data['gas_inventory']
        quantity = validated_data['quantity']
        validated_data['total_price'] = gas_inventory.unit_price * quantity
        
        return super().create(validated_data)

class InvoiceSerializer(serializers.ModelSerializer):
    """ Serializer for Invoice model to manage invoices related to orders. """
    order_details = OrderSerializer(source='order', read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'order_details', 'invoice_number', 'is_paid',
                 'admin_approval', 'admin_approval_date', 'payment_date', 'created_at']
        read_only_fields = ['invoice_number', 'admin_approval', 'admin_approval_date', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    """ Serializer for Payment model to manage payments related to invoices. """
    invoice_details = InvoiceSerializer(source='invoice', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'invoice_details', 'amount', 'status', 
                 'transaction_id', 'payment_method', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    """ Serializer for Rating model to manage ratings and comments on orders. """
    buyer_name = serializers.ReadOnlyField(source='order.buyer.username')
    seller_name = serializers.ReadOnlyField(source='order.gas_inventory.seller.username')
    
    class Meta:
        model = Rating
        fields = ['id', 'order', 'buyer_name', 'seller_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Serializer for user registration including additional fields for user profile. """
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.USER_ROLES)
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number', 'address']
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        phone_number = validated_data.pop('phone_number', None)
        address = validated_data.pop('address', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=phone_number,
            address=address
        )
        
        return user

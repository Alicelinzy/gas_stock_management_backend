from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile, GasInventory, Order, Invoice

class EndpointTests(TestCase):
    def setUp(self):
        # Create test users with different roles
        self.admin_user = User.objects.create_user('admin', 'admin@test.com', 'password123')
        self.seller_user = User.objects.create_user('seller', 'seller@test.com', 'password123')
        self.buyer_user = User.objects.create_user('buyer', 'buyer@test.com', 'password123')
        
        # Create user profiles
        UserProfile.objects.create(user=self.admin_user, role='ADMIN')
        UserProfile.objects.create(user=self.seller_user, role='SELLER')
        UserProfile.objects.create(user=self.buyer_user, role='BUYER')
        
        # Create inventory for testing
        self.inventory = GasInventory.objects.create(
            seller=self.seller_user,
            brand='TestBrand',
            weight_kg=12.0,
            quantity=10,
            unit_price=1000,
            location='Test Location'
        )
        
        # Create a test order
        self.order = Order.objects.create(
            buyer=self.buyer_user,
            gas_inventory=self.inventory,
            quantity=2,
            total_price=2000,
            status='PENDING'
        )
        
        # Create a test invoice for the order
        self.invoice = Invoice.objects.create(
            order=self.order,
            amount=2000,
            admin_approval=False,
            is_paid=False
        )
        
        # Setup API client
        self.client = APIClient()
        
    def test_gas_inventory_list(self):
        """Test that gas inventory listing works"""
        url = reverse('v1-gas-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should have our test inventory
        
    def test_gas_inventory_filter(self):
        """Test filtering gas inventory by brand"""
        url = reverse('v1-gas-list')
        response = self.client.get(url, {'brand': 'TestBrand'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Test with a non-existent brand
        response = self.client.get(url, {'brand': 'NonExistentBrand'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_order_creation_buyer(self):
        """Test that a buyer can create an order"""
        self.client.force_authenticate(user=self.buyer_user)
        url = reverse('v1-orders')
        data = {
            'gas_inventory': self.inventory.id,
            'quantity': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_order_creation_not_buyer(self):
        """Test that non-buyers cannot create orders"""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('v1-orders')
        data = {
            'gas_inventory': self.inventory.id,
            'quantity': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_order_approval_admin(self):
        """Test that an admin can approve an order"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('order-approve', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the order status has been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'APPROVED')
        
    def test_order_approval_not_admin(self):
        """Test that non-admins cannot approve orders"""
        self.client.force_authenticate(user=self.buyer_user)
        url = reverse('order-approve', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the order status has not been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'PENDING')
        
    def test_order_cancellation_buyer(self):
        """Test that a buyer can cancel their order"""
        self.client.force_authenticate(user=self.buyer_user)
        url = reverse('order-cancel', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the order status has been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'CANCELLED')
        
    def test_order_cancellation_not_buyer(self):
        """Test that non-buyers cannot cancel the order"""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('order-cancel', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the order status has not been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'PENDING')
        
    def test_mark_order_delivered_seller(self):
        """Test that a seller can mark an order as delivered"""
        # First approve the order
        self.order.status = 'APPROVED'
        self.order.save()
        
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('order-mark-delivered', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the order status has been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'DELIVERED')
        
    def test_mark_order_delivered_not_seller(self):
        """Test that non-sellers cannot mark an order as delivered"""
        # First approve the order
        self.order.status = 'APPROVED'
        self.order.save()
        
        self.client.force_authenticate(user=self.buyer_user)
        url = reverse('order-mark-delivered', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the order status has not been updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'APPROVED')
        
    def test_invoice_approval_admin(self):
        """Test that an admin can approve an invoice"""
        # Make sure order is approved first
        self.order.status = 'APPROVED'
        self.order.save()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('invoice-approve', args=[self.invoice.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the invoice has been approved
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.admin_approval)
        
    def test_invoice_approval_not_admin(self):
        """Test that non-admins cannot approve invoices"""
        # Make sure order is approved first
        self.order.status = 'APPROVED'
        self.order.save()
        
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('invoice-approve', args=[self.invoice.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the invoice has not been approved
        self.invoice.refresh_from_db()
        self.assertFalse(self.invoice.admin_approval)
        
    def test_mark_invoice_paid_admin(self):
        """Test that an admin can mark an invoice as paid"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('invoice-mark-as-paid', args=[self.invoice.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the invoice has been marked as paid
        self.invoice.refresh_from_db()
        self.assertTrue(self.invoice.is_paid)
        
    def test_mark_invoice_paid_not_admin(self):
        """Test that non-admins cannot mark invoices as paid"""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('invoice-mark-as-paid', args=[self.invoice.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the invoice has not been marked as paid
        self.invoice.refresh_from_db()
        self.assertFalse(self.invoice.is_paid) 
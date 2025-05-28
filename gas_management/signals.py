from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order, Invoice

@receiver(post_save, sender=Order)
def create_invoice_when_order_approved(sender, instance, created, **kwargs):
    Create

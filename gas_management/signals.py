from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order, Invoice

@receiver(post_save, sender=Order)
def create_invoice_when_order_approved(sender, instance, created, **kwargs):
    # Only create invoice when order is approved
    if instance.status == 'APPROVED' and not Invoice.objects.filter(order=instance).exists():
        Invoice.objects.create(
            order=instance,
            amount=instance.total_amount,
            due_date=timezone.now() + timezone.timedelta(days=7),
            admin_approval=False
        )

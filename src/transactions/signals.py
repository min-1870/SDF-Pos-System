from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TransactionProduct

@receiver([post_save, post_delete], sender=TransactionProduct)
def on_product_change_recalc(sender, instance, **kwargs):
    if instance.transaction_id:
        instance.transaction.recalculate_summary()

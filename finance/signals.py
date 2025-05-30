from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from .models import PayLoan, SupplierPayment, MenPowerPayment, DevitTransactionHistory

@receiver(post_save, sender=PayLoan)
@receiver(post_save, sender=SupplierPayment)
@receiver(post_save, sender=MenPowerPayment)
def create_transaction_history(sender, instance, created, **kwargs):
    if created:
        DevitTransactionHistory.objects.create(
            amount=instance.amount,
            payment_type=getattr(instance, 'payloan_giver_type', None) or getattr(instance, 'type', None),
            bank_account=getattr(instance, 'bank_account', None),
            check_number=getattr(instance, 'cheque_number', None) or getattr(instance, 'check_number', None),
            note=getattr(instance, 'note', ''),
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.id
        )
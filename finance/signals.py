from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from .models import PayLoan, SupplierPayment, MenPowerPayment, DevitTransactionHistory

@receiver(post_save, sender=PayLoan)
@receiver(post_save, sender=SupplierPayment)
@receiver(post_save, sender=MenPowerPayment)
def create_transaction_history(sender, instance, created, **kwargs):
    if not created:
        return

    # Determine the payment type
    payment_type = getattr(instance, 'payloan_giver_type', None) or getattr(instance, 'type', None)

    # Determine bank account and check number
    bank_account = getattr(instance, 'bank_account', None)
    check_number = getattr(instance, 'cheque_number', None) or getattr(instance, 'check_number', None)
    note = getattr(instance, 'note', '')

    # Determine project or loan provider name
    project_or_loan_name = None
    if isinstance(instance, PayLoan):
        project_or_loan_name = instance.loan.loan_provider_name
    elif isinstance(instance, SupplierPayment):
        project_or_loan_name = instance.memo.project.name
    elif isinstance(instance, MenPowerPayment):
        project_or_loan_name = instance.menpowermemo.project.name

    # Create transaction history
    DevitTransactionHistory.objects.create(
        amount=instance.amount,
        payment_type=payment_type,
        bank_account=bank_account,
        check_number=check_number,
        note=note,
        project_or_loan_name=project_or_loan_name,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.id
    )
# Generated by Django 5.1.2 on 2025-05-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_alter_bankaccount_account_type_alter_loan_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='payment_amount',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('APPROVED', 'Loan Approved'), ('PAID', 'Payment Done')], default='PENDING', max_length=10, null=True),
        ),
    ]

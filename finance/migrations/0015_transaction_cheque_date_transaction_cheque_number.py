# Generated by Django 5.1.2 on 2025-05-26 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_alter_transaction_voucher_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cheque_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='cheque_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

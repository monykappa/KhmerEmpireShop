# Generated by Django 5.0.4 on 2024-05-31 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes'),
        ),
    ]
# Generated by Django 5.0.4 on 2024-05-30 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]

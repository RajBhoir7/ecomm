# Generated by Django 3.1.8 on 2024-11-26 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='minimum_amount',
            new_name='min_amount',
        ),
    ]

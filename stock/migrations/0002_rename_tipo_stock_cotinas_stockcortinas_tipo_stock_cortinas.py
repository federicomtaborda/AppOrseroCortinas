# Generated by Django 5.1.6 on 2025-03-28 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockcortinas',
            old_name='tipo_stock_cotinas',
            new_name='tipo_stock_cortinas',
        ),
    ]

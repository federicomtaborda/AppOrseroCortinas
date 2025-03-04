# Generated by Django 5.1.6 on 2025-03-02 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_alter_cliente_direccion_alter_cliente_email_and_more'),
        ('ordendetrabajo', '0007_remove_ordentrabajo_ganancia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordentrabajo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cliente.cliente', verbose_name='Cliente'),
        ),
    ]

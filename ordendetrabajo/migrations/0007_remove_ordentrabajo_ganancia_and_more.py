# Generated by Django 5.1.6 on 2025-03-02 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordendetrabajo', '0006_alter_ordentrabajo_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordentrabajo',
            name='ganancia',
        ),
        migrations.RemoveField(
            model_name='ordentrabajo',
            name='porcentaje_ganancia',
        ),
    ]

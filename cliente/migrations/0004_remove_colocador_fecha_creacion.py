# Generated by Django 5.1.6 on 2025-03-02 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_colocador_alter_cliente_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colocador',
            name='fecha_creacion',
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-21 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0003_tipocortina_cadena_tipocortina_peso_cadena_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipocortina',
            name='cadena',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cadena'),
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-27 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ordendetrabajo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCortina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Tipo de Cortina')),
                ('alto', models.CharField(help_text='160', max_length=50, verbose_name='Medidas')),
                ('ancho', models.CharField(help_text='120', max_length=50, verbose_name='Medidas')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio Unitario')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipos_cortina', to='ordendetrabajo.ordentrabajo')),
            ],
            options={
                'verbose_name': 'Tipo de Cortina',
                'verbose_name_plural': 'Tipos de Cortina',
            },
        ),
    ]

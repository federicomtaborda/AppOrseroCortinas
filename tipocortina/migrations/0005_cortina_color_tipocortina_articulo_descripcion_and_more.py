# Generated by Django 5.1.6 on 2025-03-18 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordendetrabajo', '0001_initial'),
        ('tipocortina', '0004_remove_tipocortina_precio_venta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cortina',
            name='color',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Color'),
        ),
        migrations.AddField(
            model_name='tipocortina',
            name='articulo_descripcion',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='Art Descripción'),
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='articulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cortina', to='tipocortina.cortina'),
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='orden_trabajo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ordendetrabajo.ordentrabajo', verbose_name='Orden Trabajo'),
        ),
    ]

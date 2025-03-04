# Generated by Django 5.1.6 on 2025-02-27 20:06

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordendetrabajo', '0002_alter_ordentrabajo_cliente'),
        ('tipocortina', '0002_alter_tipocortina_alto_alter_tipocortina_ancho'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cortina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True, verbose_name='Tipo Cortina')),
            ],
            options={
                'verbose_name': 'Tipo de Cortina',
                'verbose_name_plural': 'Tipos de Cortina',
            },
        ),
        migrations.AlterModelOptions(
            name='tipocortina',
            options={'verbose_name': 'Atributo', 'verbose_name_plural': 'Atributos'},
        ),
        migrations.RemoveField(
            model_name='tipocortina',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='tipocortina',
            name='precio_unitario',
        ),
        migrations.AddField(
            model_name='tipocortina',
            name='costo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Costo Unitario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='cantidad',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orden_cortina', to='ordendetrabajo.ordentrabajo'),
        ),
        migrations.AddField(
            model_name='tipocortina',
            name='articulo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cortina', to='tipocortina.cortina'),
            preserve_default=False,
        ),
    ]

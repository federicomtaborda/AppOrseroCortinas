# Generated by Django 5.1.6 on 2025-03-10 08:27

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoMovimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('egreso', models.BooleanField(default=False, verbose_name='Egreso de Dinero')),
            ],
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_mov', models.BigIntegerField(editable=False, unique=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='monto')),
                ('detalle', models.TextField(blank=True, null=True, verbose_name='Detalle')),
                ('fecha', models.DateField(default=datetime.date.today, verbose_name='Fecha Mov')),
                ('tipo_movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movimiento.tipomovimiento', verbose_name='Tipo Movimiento')),
            ],
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-27 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordendetrabajo', '0003_rename_descripcion_ordentrabajo_observaciones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordentrabajo',
            name='estado_orden',
            field=models.CharField(choices=[('pendiente', 'pendiente'), ('demorada', 'demorada'), ('terminada', 'terminada')], default='pendiente', max_length=50),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-02 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0010_modelo_alter_cortina_modelo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cortina',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Cortina'),
        ),
        migrations.AlterField(
            model_name='modelo',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Modelo'),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-02 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0007_remove_tipocortina_orden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipocortina',
            options={'verbose_name': 'Cortina', 'verbose_name_plural': 'Cortinas'},
        ),
        migrations.AddField(
            model_name='cortina',
            name='tipo_cortina',
            field=models.BooleanField(default=False, verbose_name='Cortina de Confección '),
        ),
        migrations.AlterField(
            model_name='cortina',
            name='nombre',
            field=models.CharField(max_length=150, unique=True, verbose_name='Cortina'),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-02 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0013_tipocortina_alto_tipocortina_ancho'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocortina',
            name='mando_derecho',
            field=models.BooleanField(default=False, verbose_name='Mando Derecho'),
        ),
        migrations.AddField(
            model_name='tipocortina',
            name='mando_izquierdo',
            field=models.BooleanField(default=False, verbose_name='Mando Izquierdo'),
        ),
    ]

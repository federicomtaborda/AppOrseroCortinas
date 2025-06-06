# Generated by Django 5.1.6 on 2025-03-27 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0006_tipocortina_ancho_tubo_alter_tipocortina_cadena_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Ambiente',
                'verbose_name_plural': 'Ambientes',
            },
        ),
        migrations.AddConstraint(
            model_name='tipocaida',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_tipocaidae_name'),
        ),
        migrations.AddConstraint(
            model_name='tipomando',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_tipomando_name'),
        ),
        migrations.AddConstraint(
            model_name='tipotubo',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_tipotubo_name'),
        ),
        migrations.AddConstraint(
            model_name='ambiente',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_ambiente_name'),
        ),
        migrations.AddField(
            model_name='tipocortina',
            name='ambiente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ambiente', to='tipocortina.ambiente'),
        ),
    ]

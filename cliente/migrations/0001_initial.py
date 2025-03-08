# Generated by Django 5.1.6 on 2025-02-27 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=100, unique=True, verbose_name='Razón social')),
                ('direccion', models.TextField(max_length=100, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=25, verbose_name='Telefono')),
                ('email', models.EmailField(max_length=25, verbose_name='Email')),
            ],
        ),
    ]

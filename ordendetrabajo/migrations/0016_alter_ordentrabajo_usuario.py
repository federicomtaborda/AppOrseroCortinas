# Generated by Django 5.1.6 on 2025-03-03 13:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordendetrabajo', '0015_alter_ordentrabajo_usuario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordentrabajo',
            name='usuario',
            field=models.ForeignKey(auto_created=True, default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creador'),
            preserve_default=False,
        ),
    ]

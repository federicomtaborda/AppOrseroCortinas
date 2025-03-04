import datetime

from django.db import models



class Cliente(models.Model):
    razon_social = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Razón social')

    fecha_creacion = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha de Creación'
    )

    direccion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Dirección'
    )

    telefono = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name='Teléfono'
    )

    email = models.EmailField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name='Email'
    )

    def save(self, *args, **kwargs):
        self.nombre = self.razon_social.upper()
        super(Cliente, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social


class Colocador(models.Model):
    nombre = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Razón social'
    )

    fecha_creacion = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha de Creación'
    )

    telefono = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name='Teléfono'
    )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Colocador, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Colocador'
        verbose_name_plural = 'Colocadores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

from django.db import models


class Propietario(models.Model):
    nombre = models.CharField(u'Nombre', max_length=100)
    direccion = models.CharField(u'Dirección', max_length=100)
    telefono = models.CharField(u'Telefono', max_length=50)
    ciudad = models.CharField(u'Ciudad', max_length=50)
    cod_postal = models.IntegerField(u'CP')
    email = models.CharField(u'Email', max_length=100, null=True , blank=True)
    cbu = models.CharField(u'CBU', max_length=50, null=True , blank=True)


    class Meta:
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietario'

    def __str__(self):
        return self.nombre
from django.core.validators import MinValueValidator
from django.db import models


class variablesModels(models.Model):
    var_cadena = models.DecimalField(
        verbose_name='Variable Cadena',
        decimal_places=2,
        max_digits=6,
        help_text='Valor de la variable cadena',
        default=0,
        validators=[MinValueValidator(0)]
    )

    var_enrolle = models.DecimalField(
        verbose_name='Variable Enrolle',
        decimal_places=2,
        max_digits=6,
        help_text='Valor agregado de tela enrolle',
        default=0,
        validators=[MinValueValidator(0)]
    )

    var_tapa_zocalos = models.DecimalField(
        verbose_name='Tapa Zocalos',
        decimal_places=2,
        max_digits=6,
        help_text='2 zolalos por cortina',
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Variables Generales'
        verbose_name_plural = 'Variables Generales'

    def __str__(self):
        return 'Varibles Generales'

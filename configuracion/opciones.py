class TipoStock:
    INGRESO = 'Ingreso'
    EGRESO = 'Egreso'


TIPO_STOCK = (
    (TipoStock.INGRESO, "Ingreso de Stock"),
    (TipoStock.EGRESO, "Egreso de Stock"),
)


class EstadoStock:
    COMPROMETIDO = 'Ingreso'
    APLICADO = 'Egreso'


ESTADO_STOCK = (
    (EstadoStock.COMPROMETIDO, "Comprometido"),
    (EstadoStock.APLICADO, "Aplicado"),
)

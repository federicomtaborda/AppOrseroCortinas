jQuery(function ($) {

    $(document).ready(function () {
        // Variables globales
        const globalVars = {
            cadena: 0,
            enrolle: 0,
            tapaZocalos: 0
        };

        // Cache de elementos del DOM
        const $elements = {
            costoTotal: $('#id_costo_total'),
            gananciaNeta: $('#id_ganancia_neta'),
            total: $('#id_total'),
            costo: $('#id_costo'),
            cantidad: $('#id_cantidad'),
            costoManoObra: $('#id_costo_mano_obra'),
            otrosCostos: $('#id_otros_costos'),
            gananciaPorcentaje: $('#id_ganancia_porcentaje'),
            alto: $('#id_alto'),
            ancho: $('#id_ancho'),
            articulo: $('#id_articulo'),
            cadena: $('#id_cadena'),
            zocalo: $('#id_zocalo'),
            tapaZocalo: $('#id_tapa_zocalo'),
            pesoCadena: $('#id_peso_cadena'),
            tope: $('#id_tope'),
            union: $('#id_union'),
            anchoTubo: $('#id_ancho_tubo'),
            metrosTotales: $('#id_metros_totales'),
            form: $('#tipocortina_form')
        };

        // Deshabilitar focus en campos de totales
        $elements.costoTotal.add($elements.gananciaNeta).add($elements.total).attr('tabindex', '-1');

        // Función para calcular el total
        function calcularTotal() {
            const costoUnitario = parseFloat($elements.costo.val()) || 0;
            const costoManoObra = parseFloat($elements.costoManoObra.val()) || 0;
            const otrosCostos = parseFloat($elements.otrosCostos.val()) || 0;
            const gananciaPorcentaje = parseFloat($elements.gananciaPorcentaje.val()) || 0;
            const cantidad = parseFloat($elements.cantidad.val()) || 0;

            // Calcular costo total
            const totalCosto = (costoUnitario + costoManoObra + otrosCostos) * cantidad;
            const gananciaNeta = totalCosto * (gananciaPorcentaje / 100);
            const totalFinal = totalCosto + gananciaNeta;

            // Actualizar campos
            $elements.costoTotal.val(totalCosto.toFixed(2));
            $elements.gananciaNeta.val(gananciaNeta.toFixed(2));
            $elements.total.val(totalFinal.toFixed(2));
        }

        // Función para obtener variables de configuración
        function calcularInsumos() {
            return $.ajax({
                url: '/tipocortina/get_variables_config/',
                type: 'GET',
                dataType: 'json'
            }).then(function(response) {
                if (response.variables && response.variables.length > 0) {
                    const variables = response.variables[0];
                    globalVars.cadena = variables.var_cadena;
                    globalVars.enrolle = variables.var_enrolle;
                    globalVars.tapaZocalos = variables.var_tapa_zocalos;
                }
                return globalVars;
            }).fail(function(xhr, status, error) {
                console.log('Error al obtener variables:', error);
                return globalVars;
            });
        }

        // Función para actualizar campos de insumos
        function actualizarCampos() {
            calcularInsumos().then(function() {
                const alto = parseFloat($elements.alto.val()) || 0;
                const ancho = parseFloat($elements.ancho.val()) || 0;
                const cantidad = parseFloat($elements.cantidad.val()) || 0;

                // Calcular insumos
                const idCadena = globalVars.cadena * alto * cantidad;
                const idTapaZocalo = globalVars.tapaZocalos * cantidad;
                const idMetrosTotales = (alto + parseFloat(globalVars.enrolle)) * ancho * cantidad;

                // Actualizar campos
                $elements.cadena.val(idCadena.toFixed(2));
                $elements.zocalo.val((ancho * cantidad).toFixed(2));
                $elements.tapaZocalo.val(idTapaZocalo);
                $elements.pesoCadena.val(cantidad);
                $elements.tope.val(cantidad);
                $elements.union.val(cantidad);
                $elements.anchoTubo.val((ancho * cantidad).toFixed(2));
                $elements.metrosTotales.val(idMetrosTotales.toFixed(2));
            });
        }

        // Función para calcular costo basado en artículo
        function calcularCosto() {
            const idArticulo = parseFloat($elements.articulo.val()) || 0;
            const cantidad = parseFloat($elements.cantidad.val()) || 0;
            const alto = parseFloat($elements.alto.val()) || 0;
            const ancho = parseFloat($elements.ancho.val()) || 0;

            if (!idArticulo) return;

            $.ajax({
                url: `/tipocortina/costo_m2/${idArticulo}`,
                type: 'GET',
                dataType: 'json'
            }).done(function(costoM2) {
                const res = parseFloat(alto * ancho * costoM2 * cantidad);
                $elements.costo.val(res.toFixed(2));
                calcularTotal();
            }).fail(function(xhr, status, error) {
                console.error("Error al obtener costo m2:", error);
            });
        }

        // Función para manejar cambio de artículo
        function handleArticuloChange() {
            const articleId = $elements.articulo.val();
            if (!articleId) return;

            $.ajax({
                url: `/tipocortina/get_fabricacion/${articleId}`,
                type: 'GET',
                dataType: 'json'
            }).done(function(fabricacion) {
                const fieldsets = $elements.form.find('> div > fieldset').slice(2, 6);
                const valueFields = ['#id_cantidad', '#id_alto', '#id_ancho'];
                const calculationFields = [
                    '#id_ganancia_porcentaje',
                    '#id_ganancia_neta',
                    '#id_total',
                    '#id_costo_total'
                ];
                const selectFields = ['#id_mando', '#id_caida', '#id_tubo', '#id_ambiente'];

                fieldsets.css('display', fabricacion ? '' : 'none');
                $(valueFields.join(',')).val(0);
                $(calculationFields.join(',')).val('0.00');
                selectFields.forEach(selector => $(selector).val(null).trigger('change'));

                actualizarCampos();
            }).fail(function(xhr, status, error) {
                console.error("Error al obtener fabricación cortina:", error);
            });
        }

        // Event listeners
        $elements.costo.add($elements.cantidad).add($elements.costoManoObra)
            .add($elements.otrosCostos).add($elements.gananciaPorcentaje)
            .on('input', calcularTotal);

        $elements.alto.add($elements.ancho).add($elements.cantidad)
            .on('input', actualizarCampos);

        $elements.alto.add($elements.ancho).add($elements.cantidad)
            .add($elements.articulo).on('input change', calcularCosto);

        $elements.articulo.on('change', handleArticuloChange);

        // Inicialización
        calcularTotal();
        actualizarCampos();
    });
});
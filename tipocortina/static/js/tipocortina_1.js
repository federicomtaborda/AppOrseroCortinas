jQuery(function ($) {

    $(document).ready(function () {

        var globalVarCadena = 0;
        var globalVarEnrolle = 0;
        var globalVarTapaZocalos = 0;

        /* no permite tomar el focus*/
        $("#id_costo_total, #id_ganancia_neta, #id_total").attr("tabindex", "-1");

        // Función para calcular el total
        function calcularTotal() {
            let costo_unitario = parseFloat($('#id_costo').val()) || 0;
            let costo_mano_obra = parseFloat($('#id_costo_mano_obra').val()) || 0;
            let otros_costos = parseFloat($('#id_otros_costos').val()) || 0;
            let ganancia_porcentaje = parseFloat($('#id_ganancia_porcentaje').val()) || 0;

            let cantidad = parseFloat($('#id_cantidad').val()) || 0;

            // Calcular costo total
            let total_costo = (costo_unitario + costo_mano_obra + otros_costos) * cantidad;

            // Calcular ganancia neta basada en el porcentaje
            let ganancia_neta = total_costo * (ganancia_porcentaje / 100);

            // Calcular total final (costo total + ganancia neta)
            let total_final = total_costo + ganancia_neta;

            // Actualizar los campos
            $('#id_costo_total').val(total_costo.toFixed(2));
            $('#id_ganancia_neta').val(ganancia_neta.toFixed(2));
            $('#id_total').val(total_final.toFixed(2));
        }

        // Escuchar cambios en los campos de entrada
        $('#id_costo, #id_cantidad, #id_costo_mano_obra, #id_otros_costos, #id_ganancia_porcentaje').on('input', function () {
            calcularTotal();
        });

        // Calcular el total inicialmente por si ya hay valores
        calcularTotal();


        function calcularInsumos() {
            return $.ajax({
                url: '/tipocortina/get_variables_config/',
                type: 'GET',
                dataType: 'json',
                success: function (response) {
                    if (response.variables && response.variables.length > 0) {
                        let variables = response.variables[0];
                        globalVarCadena = variables.var_cadena;
                        globalVarEnrolle = variables.var_enrolle;
                        globalVarTapaZocalos = variables.var_tapa_zocalos;
                    }
                },
                error: function (xhr, status, error) {
                    console.log(error);
                }
            });
        }

        function actualizarCampos() {
            calcularInsumos().then(function () {
                let alto = parseFloat($('#id_alto').val()) || 0;
                let ancho = parseFloat($('#id_ancho').val()) || 0;
                let cantidad = parseFloat($('#id_cantidad').val()) || 0;


                // insumos
                let id_cadena = globalVarCadena * alto * cantidad;
                let id_tapa_zocalo = globalVarTapaZocalos * cantidad;
                let id_metros_totales = (alto + parseFloat(globalVarEnrolle)) * ancho * cantidad;

                // Actualizar los campos
                $('#id_cadena').val(id_cadena.toFixed(2));
                $('#id_zocalo').val(ancho.toFixed(2));
                $('#id_tapa_zocalo').val(id_tapa_zocalo);
                $('#id_peso_cadena').val(cantidad);
                $('#id_tope').val(cantidad);
                $('#id_union').val(cantidad);
                $('#id_metros_totales').val(id_metros_totales.toFixed(2));
            });
        }

        $("#id_alto, #id_ancho, #id_cantidad").on('input', function () {
            actualizarCampos();
        });

        $("#id_articulo").on('change', function () {

        });

        function calcularCosto(art_id) {
            let id_articulo = parseFloat($('#id_articulo').val()) || 0;
            let cantidad = parseFloat($('#id_cantidad').val()) || 0;
            let alto = parseFloat($('#id_alto').val()) || 0;
            let ancho = parseFloat($('#id_ancho').val()) || 0;


            $.ajax({
                url: '/tipocortina/costo_2/' + id_articulo,
                type: 'GET',
                dataType: 'json',
                success: function (costo_2) {
                    const res = parseFloat(parseFloat(alto * ancho) * costo_2 * cantidad);
                    $('#id_costo').val(res.toFixed(2));
                    console.log(res);
                },
                error: function (xhr, status, error) {
                    console.error("Error al obtener costo m2:", error);
                }
            });
        }

        // $("#id_articulo").on('change', function () {
        //     calcularCosto();
        // });

        $("#id_alto, #id_ancho, #id_cantidad, #id_articulo").on('input change', function () {
            calcularCosto();
        });

        actualizarCampos();

    });//fin ready

});
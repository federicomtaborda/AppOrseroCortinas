jQuery(function ($) {

    $(document).ready(function () {
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
    });

});
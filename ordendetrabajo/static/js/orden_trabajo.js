jQuery(function ($) {

    $(document).ready(function () {
        /* no permite tomar el focus*/
        $("#id_total").attr("tabindex", "-1");

        function calculateTotal() {
            // Get the number of rows
            const $totalForms = $('#id_tipocortina_set-TOTAL_FORMS');
            const rows = parseInt($totalForms.val()) || 0;

            // Initialize total
            let total = 0;

            // Calculate total only if there are rows
            if (rows > 0) {
                for (let x = 0; x < rows; x++) {
                    // Get price value and convert to float, default to 0 if invalid
                    totalValue = parseFloat($(`#id_tipocortina_set-${x}-total`).val());
                    total += totalValue;
                }
            }

            // Si form read only total isNAN corto la ejecucion y muestro total guardado
            if (Number.isNaN(total)) {
                return;
            } else {
                $('#id_total').val(total.toFixed(2));
            }
        }

        // Initial calculation
        calculateTotal();

        $('[id^="id_tipocortina_set-"][id$="-total"]').on('input', calculateTotal);
    });
});
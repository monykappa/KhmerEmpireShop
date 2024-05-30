$(document).ready(function () {
    $('#add-to-cart-form').on('submit', function (event) {
        event.preventDefault();

        var $form = $(this);
        var url = $form.attr('action');
        var data = $form.serialize();

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
                }
            }
        });

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: function (response) {
                Swal.fire({
                    title: 'Success',
                    text: 'Product added to cart successfully!',
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            },
            error: function (response) {
                Swal.fire({
                    title: 'Error',
                    text: 'There was a problem adding the product to the cart.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});

// Create our number formatter.
var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
});

var updatePrice = function() {
    var total_price = 0;
    $('.item-card').each(function(index) {
        var cart_item = $(this).children('.cart-item');;
        var quantity = cart_item.data('quantity');
        var price = cart_item.data('price');
        console.log(cart_item);
        total_price += price * quantity;
    });
    $('#cart-total-price').html(formatter.format(total_price));
};

$(document).ready(function() {
    $(document).on("click", ".cart-item-trash", function() {
        var cart_item = $(this).parent('div').parent('div').parent('div').children('.cart-item');
        var quantity = cart_item.data('quantity', 0);
        cart_item.parent('div').hide();
        updatePrice();
    });

    $(document).on("click", ".minus", function() {
        var cart_item = $(this).parent('.btn-group').parent('div').parent('.cart-item');
        var quantity = cart_item.data('quantity');
        var max = cart_item.data('max');
        var price = cart_item.data('price');
        var quantity_display = $(this).parent('.btn-group').children('.quantity-display');
        var price_display = cart_item.children('div').children('.price-display');

        if (quantity != 0) {
            quantity -= 1;
            quantity_display.html(quantity);
            cart_item.data('quantity', quantity);
            price_display.html(formatter.format(quantity * price));
        }

        if (quantity == 1) {
            $(this).html('<i class="fa fa-trash align-middle" aria-hidden="true"></i>');
        }

        if (quantity == 0) {
            $(this).parent('.btn-group').parent('div').parent('.cart-item').parent('div').hide();
        }

        if (quantity != max) {
            $(this).parent('.btn-group').children('.plus').prop('disabled', false);
            $(this).parent('.btn-group').children('.plus').css("background-color", '#0d6efd');
        }
        updatePrice();

    });

    $(document).on("click", ".plus", function() {
        var cart_item = $(this).parent('.btn-group').parent('div').parent('.cart-item');
        var quantity = cart_item.data('quantity');
        var max = cart_item.data('max');
        var price = cart_item.data('price');
        var quantity_display = $(this).parent('.btn-group').children('.quantity-display');
        var price_display = cart_item.children('div').children('.price-display');

        if (quantity != max) {
            quantity += 1;
            quantity_display.html(quantity);
            cart_item.data('quantity', quantity);
            price_display.html(formatter.format(quantity * price));
        }
        if (quantity == max) {
            $(this).prop('disabled', true);
            $(this).css("background-color", '#484848');
        }
        updatePrice();
    });
});
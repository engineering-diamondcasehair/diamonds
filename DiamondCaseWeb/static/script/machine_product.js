$(document).on('click', '.add-to-cart-btn', function() {
    var quantity_element = $(this).parent('.quantity');
    var machine_id = quantity_element.children('.btn-group').data('id');
    var quantity = quantity_element.data('quantity');
    var max = quantity_element.data('max');
    var button_group = quantity_element.children('.btn-group');

    if (quantity != max) {
        quantity += 1;
        quantity_element.data("quantity", quantity);
        button_group.children('.shop-product-quantity').html(quantity);
    }

    if (!quantity == max) {
        button_group.children('.plus').prop("disabled", true);
    }

    $(this).hide();
    button_group.show();
});

$(document).on('click', '.minus', function() {
    var quantity_element = $(this).parents('.quantity');
    var machine_id = quantity_element.children('.btn-group').data('id');
    var quantity = quantity_element.data('quantity');
    var max = quantity_element.data('max');
    var button_group = quantity_element.children('.btn-group');
    var add_to_cart_button = quantity_element.children('.add-to-cart-btn');

    if (quantity != 0) {
        quantity -= 1;
        quantity_element.data("quantity", quantity);
        button_group.children('.shop-product-quantity').html(' ' + quantity + ' ');
    }

    if (quantity == 0) {
        button_group.hide();
        add_to_cart_button.show()
    } else if (quantity != max) {
        button_group.children('.plus').prop("disabled", false);
    }

});


$(document).on('click', '.plus', function() {
    var quantity_element = $(this).parents('.quantity');
    var machine_id = quantity_element.children('.btn-group').data('id');
    var quantity = quantity_element.data('quantity');
    var max = quantity_element.data('max');
    var button_group = quantity_element.children('.btn-group');
    var add_to_cart_button = quantity_element.children('.add-to-cart-btn');

    if (quantity != max) {
        quantity += 1;
        quantity_element.data("quantity", quantity);
        button_group.children('.shop-product-quantity').html(' ' + quantity + ' ');
    } else {
        alert("Sorry this is all we have.");
    }

    if (quantity == max) {
        button_group.children('.plus').prop("disabled", true);
    }
});


setInterval(function() {
    if ($(window).width() < 576) {
        $('#product-menu-header').hide();
    } else {
        $('#product-menu-header').show();
    }
}, 500);

window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;
    if (window.pageYOffset > 145 &&
        !$("#product-menu-header").hasClass("fixed-top")) {
        $("#product-menu-header").addClass("fixed-top");

    } else if (window.pageYOffset <= 145 &&
        $("#product-menu-header").hasClass("fixed-top")) {
        $("#product-menu-header").removeClass("fixed-top");
    }
});
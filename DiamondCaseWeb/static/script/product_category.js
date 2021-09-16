var number_of_pages;
var page_size = 6.0;
var current_page = 0;

var pagationSetup = function(page) {
    number_of_pages = Math.ceil($('#product-category-view').children('#product-category-card').length / page_size);

    $('.pagination').append('<li class="page-item" onclick="tranversePage(true);"><a class="page-link" href="#" >Previous</a></li>');
    for (var i = 0; i < number_of_pages; i++) {
        $('.pagination').append('<li class="page-item" data-id="' + parseInt(i) + '"><a class="page-link" href="#" onclick="doPagation(' + parseInt(i) + ');">' + parseInt(i + 1) + '</a></li>');
    }
    $('.pagination').append('<li class="page-item" onclick="tranversePage(false);"><a class="page-link" href="#">Next</a></li>');
}

var tranversePage = function(invert) {
    if (!invert) {
        if (current_page < number_of_pages - 1) {
            current_page = current_page + 1;
            doPagation(current_page);
        }
    } else {
        if (current_page > 0) {
            current_page = current_page - 1;
            doPagation(current_page);
        }
    }
}

var doPagation = function(page) {
    item_begin_idx = page * page_size;
    item_end_idx = page * page_size + page_size - 1;

    $(".product-category-product").each(function(index) {

        if (index >= item_begin_idx && index <= item_end_idx) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
};
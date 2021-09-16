var setupFixedCategoryMenu = function() {
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
};


;(function($) {

    "use strict";

    var tf_dots = function (){
        $(".item-dot").on("mouseover", function () {
            $(".item-dot").removeClass('active');
            $(this).addClass('active');
        });
        $(".item-dot").click(function() {
            $(this).toggleClass('active');
        });
    }

    

$(window).on('elementor/frontend/init', function() {
    elementorFrontend.hooks.addAction( 'frontend/element_ready/tf-list-dots.default', tf_dots );
});

})(jQuery);
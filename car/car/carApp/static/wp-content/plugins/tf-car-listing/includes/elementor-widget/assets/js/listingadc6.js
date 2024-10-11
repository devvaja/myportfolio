(function ($) {
    var listingOwlCarousel = function ($scope) {
        if ($().owlCarousel) {
            $scope.find('.tf-listing-wrap.has-carousel .owl-carousel').each(function () {
                var
                    $this = $(this),
                    item = $this.data("column"),
                    item2 = $this.data("column2"),
                    item3 = $this.data("column3"),
                    item4 = $this.data("column4"),
                    spacing = $this.data("spacing"),
                    prev_icon = $this.data("prev_icon"),
                    next_icon = $this.data("next_icon");

                var loop = false;
                if ($this.data("loop") == 'yes') {
                    loop = true;
                }

                var arrow = false;
                if ($this.data("arrow") == 'yes') {
                    arrow = true;
                }

                var bullets = false;
                if ($this.data("bullets") == 'yes') {
                    bullets = true;
                }

                var auto = false;
                if ($this.data("auto") == 'yes') {
                    auto = true;
                }
                
                $('.has-overlay').on('initialized.owl.carousel translate.owl.carousel', function(e){
                    idx = e.item.index;
                    $(this).find('.owl-item').removeClass('active_overlay');
                    $(this).find('.owl-item').eq(idx+2).addClass('active_overlay');
                });

                $this.owlCarousel({
                    loop: loop,
                    margin: spacing,
                    nav: arrow,
                    dots: bullets,
                    autoplay: auto,
                    autoplayTimeout: 5000,
                    smartSpeed: 850,
                    autoplayHoverPause: true,
                    navText: ["<i class=\"" + prev_icon + "\"></i>", "<i class=\"" + next_icon + "\"></i>"],
                    responsive: {
                        0: {
                            items: item3
                        },
                        768: {
                            items: item2
                        },
                        1000: {
                            items: item4
                        },
                        1400: {
                            items: item
                        }
                    }
                });
            });
        }
    }

    var listingFilterTabsTaxonomy = function ($scope) {
        $scope.find('.show_filter_tabs .wrap-listing-post').each(function () {
            var $wrap_container = $(this).closest('.wrap-listing-post');
            var loading = '<span class="loading-icon"><span class="dot-flashing"></span></span>';
            $(this).children('.content-tab').children().hide();
            $(this).children('.content-tab').children().first().show().addClass('active');

            $(this).find('.filter-bar').children('a').hover(function (e) {
                e.preventDefault();
                var itemActive = $(this).index(),
                    contentActive = $(this).siblings().parents('.show_filter_tabs .wrap-listing-post').children('.content-tab').children().eq(itemActive);
                var numItems = contentActive.find('.listing').find('.item').length;
                $(this).closest('.filter-bar').find('.content').text(numItems + ' property');
            });

            $(this).find('.filter-bar').children('a').on('click', function (e) {
                e.preventDefault();

                $wrap_container.find('.content-tab').children().children().append(loading);
                var itemActive = $(this).index(),
                    contentActive = $(this).siblings().removeClass('active').parents('.show_filter_tabs .wrap-listing-post').children('.content-tab').children().eq(itemActive);
                $(this).addClass('active')
                contentActive.addClass('active').fadeIn('slow');
                var numItems = contentActive.find('.listing').find('.item').length;

                $(this).closest('.filter-bar').find('.content').text(numItems + ' property');

                contentActive.siblings().removeClass('active');
                $(this).addClass('active').parents('.show_filter_tabs .wrap-listing-post').children('.content-tab').children().eq(itemActive).siblings().hide();

                setTimeout(function () {
                    $wrap_container.find('.listing .loading-icon').fadeOut('', function () {
                        setTimeout(function () {
                            $wrap_container.find('.listing .loading-icon').remove();
                        }, 500);
                    });
                }, 700);
            });
        });
    }

    var swiperGalleryImages = function () {
        $(this).delay().queue(function () {
            new Swiper(".swiper-container.carousel-image-box", {
                slidesPerView: 1,
                spaceBetween: 30,
                navigation: {
                    clickable: true,
                    nextEl: ".swiper-button-next2",
                    prevEl: ".swiper-button-prev2",
                },
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                    dynamicBullets: true,
                    dynamicMainBullets: 1
                },
            });
            $(this).dequeue();
        });
    }

    var hoverThumbGallery = function (e) {        
        e.find('.hover-listing-image').each(function () { 
            $(this).find('.listing-item:first-child').addClass('active');
            $(this).find('.bl-item:first-child').addClass('active');
            $(".hover-listing-image .listing-item").hover(
                function () {
                  var index = $(this).index();
                  $(this).closest('.hover-listing-image').find('.listing-item').removeClass('active');
                  $(this).addClass("active");
                  $(this).closest('.hover-listing-image').find('.bl-item').removeClass('active');
                  $(this).closest('.hover-listing-image').find('.bl-item').eq(index).addClass('active');
                },
                function () {
                  $(this).removeClass("active");
                  $(this).closest('.hover-listing-image').find('.bl-item').removeClass('active');
                  $(this).closest('.hover-listing-image').find('.listing-item:first-child').addClass('active');
                  $(this).closest('.hover-listing-image').find('.bl-item:first-child').addClass('active');
                }
            );

        });
    }

    $(window).on('elementor/frontend/init', function () {
        elementorFrontend.hooks.addAction('frontend/element_ready/tf_listing_list.default', listingOwlCarousel);
        elementorFrontend.hooks.addAction('frontend/element_ready/tf_listing_list.default', function () {
            swiperGalleryImages();
            $('.show_filter_tabs .wrap-listing-post').find('.filter-bar').children('a').on('click', function (e) {
                swiperGalleryImages();
            })
        });
        elementorFrontend.hooks.addAction('frontend/element_ready/tf_listing_list.default', listingFilterTabsTaxonomy);
        elementorFrontend.hooks.addAction('frontend/element_ready/tf_listing_list.default', hoverThumbGallery);
    });
})(jQuery);
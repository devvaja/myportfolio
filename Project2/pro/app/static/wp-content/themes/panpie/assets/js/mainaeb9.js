jQuery(document).ready(function ($) {
    "use strict";
    var $grid;

    var priceselector = '.product p.price';
    var originalprice = $(priceselector).html();
    $(document).on('show_variation', function () {
        //$(priceselector).html($('.single_variation .woocommerce-variation-price').html());
        let dynamic_price = $('.single_variation .woocommerce-variation-price').html();
        if ( dynamic_price ) {
            $(priceselector).html(dynamic_price);
        }
    });
    $(document).on('hide_variation', function () {
        $(priceselector).html(originalprice);
    });


    $('a[href=\\#]').on('click', function (e) {
        e.preventDefault();
    });

    /*For varable product Add to cart - START*/

    var rt_site_url = $('.panpie-style-style1').data("url");

    $(".food-box").on('click', 'a.ajax_add_to_cart', function (e) {
        e.preventDefault();
        var self = $(this),
            productId = self.data('product-id'),
            variationId = self.data('variation-id'),
            attributeName = self.data('attribute-name'),
            attributeValue = self.data('attribute-value'),
            quantity = 1,
            item = {};
        item[attributeName] = attributeValue;
        var data = {
            action: 'rt_add_to_cart_variable_rc',
            product_id: productId,
            quantity: quantity,
            variation_id: variationId,
            variation: item
        };
        console.log(data);
        $.ajax({
            url: wc_add_to_cart_params.ajax_url,
            data: data,
            type: "POST",
            beforeSend: function () {

                $('.added_to_cart.wc-forward').remove();
                $('.view_button_tmp').remove();
                self.addClass('loading');
            },
            success: function (response) {
                var fragments = response.fragments;

                if (fragments) {

                    $.each(fragments, function (key, value) {
                        $(key).replaceWith(value);
                    });

                    $('<a href="' + rt_site_url + '/cart/" class="view_button_tmp added_to_cart wc-forward" title="View cart">View cart</a>').insertAfter(self);

                }
                self.removeClass('loading');
                $('.view_button_tmp').remove();
            },
            error: function () {

            }
        });

        return false;
    });

    /*For varable product Add to cart - END*/

    /* Isotope */
    if (typeof $.fn.isotope == 'function') {
        var $parent = $('.rt-isotope-wrapper'),
            $isotope;
        var blogGallerIso = $(".rt-isotope-content", $parent).imagesLoaded(function () {
            $isotope = $(".rt-isotope-content", $parent).isotope({
                filter: "*",
                transitionDuration: "1s",
                hiddenStyle: {
                    opacity: 0,
                    transform: "scale(0.001)"
                },
                visibleStyle: {
                    transform: "scale(1)",
                    opacity: 1
                }
            });
            $('.rt-isotope-tab a').on('click', function () {
                console.log('click');
                var $parent = $(this).closest('.rt-isotope-wrapper'),
                    selector = $(this).attr('data-filter');
                console.log($parent);
                $parent.find('.rt-isotope-tab .current').removeClass('current');
                $(this).addClass('current');
                $isotope.isotope({
                    filter: selector
                });

                return false;
            });

            $(".hide-all .rt-portfolio-tab a").first().trigger('click');
        });
    }


    /*ISOTOPE HTML START*/
    var $container = $(".isotope-wrap");
    if ($container.length > 0) {
        var $isotope;
        var blogGallerIso = $(".featuredContainer", $container).imagesLoaded(function () {
            $isotope = $(".featuredContainer", $container).isotope({
                filter: "*",
                transitionDuration: "1s",
                hiddenStyle: {
                    opacity: 0,
                    transform: "scale(0.001)"
                },
                visibleStyle: {
                    transform: "scale(1)",
                    opacity: 1
                }
            });
            $(".hide-all .isotope-classes-tab a").first().trigger('click');
        });
        $container.find(".isotope-classes-tab").on("click", "a", function () {
            var $this = $(this);
            $this
                .parent(".isotope-classes-tab")
                .find("a")
                .removeClass("current");
            $this.addClass("current");
            var selector = $this.attr("data-filter");
            $isotope.isotope({
                filter: selector
            });
            return false;
        });
    }
    /*ISOTOPE HTML END*/

    /* Theia Side Bar */
    if (typeof ($.fn.theiaStickySidebar) !== "undefined") {
        $('.has-sidebar .fixed-bar-coloum').theiaStickySidebar({'additionalMarginTop': 150});
        $('.shop-page .fixed-bar-coloum').theiaStickySidebar({'additionalMarginTop': 150});
    }

    /* Header Search */
    $('body').on("click", 'a[href="#header-search"]', function (event) {
        event.preventDefault();

        var target = $(".header-search-field");
        target.removeClass("close-change");
        target.addClass("header-search-open");

        var self_item_glass = $('a[href="#header-search"]');
        self_item_glass.addClass("close-change");
        self_item_glass.removeClass("open-change");

        var self_item_cross = $('a[href="#header-cross"]');
        self_item_cross.addClass("open-change");
        self_item_cross.removeClass("close-change");

        setTimeout(function () {
            target.find('input').focus();
        }, 600);
        return false;
    });

    $('body').on("click", 'a[href="#header-cross"]', function (event) {
        event.preventDefault();

        var target = $(".header-search-field");
        target.addClass("close-change");
        target.removeClass("header-search-open");

        var self_item_glass = $('a[href="#header-search"]');
        self_item_glass.removeClass("close-change");
        self_item_glass.addClass("open-change");

        var self_item_cross = $('a[href="#header-cross"]');
        self_item_cross.removeClass("open-change");
        self_item_cross.addClass("close-change");

        setTimeout(function () {
            target.find('input').focus();
        }, 600);
        return false;
    });

    /* masonary */
    if ($('#primary').find('div.rt-masonry-grid').length !== 0) {
        var grid = $('.rt-masonry-grid').imagesLoaded(function () {
            $grid = grid.isotope({
                // set itemSelector so .grid-sizer is not used in layout
                itemSelector: '.rt-grid-item',
                percentPosition: true,
                isAnimated: true,
                masonry: {
                    columnWidth: '.rt-grid-item',
                    horizontalOrder: true
                },
                animationOptions: {
                    duration: 700,
                    easing: 'linear',
                    queue: false
                }
            });
        });
    }
    /* Scroll to top */
    $('.scrollup').on('click', function () {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 200) {
            $('.scrollup').addClass('back-top');
        } else {
            $('.scrollup').removeClass('back-top');
        }
    });

    /* Mobile menu */
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 100) {
            $("body").addClass("not-top");
            $("body").removeClass("top");
        } else {
            $("body").addClass("top");
            $("body").removeClass("not-top");
        }
    });

    /* Search Box */
    $(".search-box-area").on('click', '.search-button, .search-close', function (event) {
        event.preventDefault();
        if ($('.search-text').hasClass('active')) {
            $('.search-text, .search-close').removeClass('active');
        } else {
            $('.search-text, .search-close').addClass('active');
        }
        return false;
    });

    /* Header Right Menu */
    var menuArea = $('.additional-menu-area');
    menuArea.on('click', '.side-menu-trigger', function (e) {
        e.preventDefault();
        var self = $(this);
        if (self.hasClass('side-menu-open')) {
            $('.sidenav').css('transform', 'translateX(0%)');
            if (!menuArea.find('> .rt-cover').length) {
                menuArea.append("<div class='rt-cover'></div>");
            }
            self.removeClass('side-menu-open').addClass('side-menu-close');
        }
    });

    function closeMenuArea() {
        var trigger = $('.side-menu-trigger', menuArea);
        trigger.removeClass('side-menu-close').addClass('side-menu-open');
        if (menuArea.find('> .rt-cover').length) {
            menuArea.find('> .rt-cover').remove();
        }
        $('.sidenav').css('transform', 'translateX(100%)');
    }

    menuArea.on('click', '.closebtn', function (e) {
        e.preventDefault();
        closeMenuArea();
    });

    $(document).on('click', '.rt-cover', function () {
        closeMenuArea();
    });

    /*-------------------------------------
    MeanMenu activation code
    --------------------------------------*/
    var a = $('.offscreen-navigation .menu');
    if (a.length) {
        $(".menu-item-has-children").append("<span></span>");
        $(".page_item_has_children").append("<span></span>");

        a.children("li").addClass("menu-item-parent");

        $('.menu-item-has-children > span').on('click', function () {
            $(this).siblings('a').first().toggleClass('opened');
            var _self = $(this),
                sub_menu = _self.parent().find('>.sub-menu');
            if (_self.hasClass('open')) {
                sub_menu.slideUp();
                _self.removeClass('open');
            } else {
                sub_menu.slideDown();
                _self.addClass('open');
            }
        });
        $('.page_item_has_children > span').on('click', function () {
            var _self = $(this),
                sub_menu = _self.parent().find('>.children');
            if (_self.hasClass('open')) {
                sub_menu.slideUp();
                _self.removeClass('open');
            } else {
                sub_menu.slideDown();
                _self.addClass('open');
            }
        });
    }

    $('.mean-bar .sidebarBtn').on('click', function (e) {
        e.preventDefault();
        if ($('.rt-slide-nav').is(":visible")) {
            $('.rt-slide-nav').slideUp();
            $('body').removeClass('slidemenuon');
        } else {
            $('.rt-slide-nav').slideDown();
        $('body').addClass('slidemenuon');
        }

    });


    /* Sticky Header */
    $(window).on('scroll', function () {
        if ($('body').hasClass('sticky-header')) {
            var stickyPlaceHolder = $("#rt-sticky-placeholder"),
                menu = $("#header-menu"),
                menuH = menu.outerHeight(),
                topHeaderH = $('#header-top-fix').outerHeight() || 0,
                middleHeaderH = $('#header-middlebar').outerHeight() || 0,
                targrtScroll = topHeaderH + middleHeaderH;
            if ($(window).scrollTop() > targrtScroll) {
                menu.addClass('rt-sticky');
                stickyPlaceHolder.height(menuH);
            } else {
                menu.removeClass('rt-sticky');
                stickyPlaceHolder.height(0);
            }
        }
    });

    /* Woocommerce Shop change view */
    $('#shop-view-mode li a').on('click', function () {
        $('body').removeClass('product-grid-view').removeClass('product-list-view');

        if ($(this).closest('li').hasClass('list-view-nav')) {
            $('body').addClass('product-list-view');
            Cookies.set('shopview', 'list');
        } else {
            $('body').addClass('product-grid-view');
            Cookies.remove('shopview');
        }
        return false;
    });

    // Popup - Used in video
    if (typeof $.fn.magnificPopup == 'function') {
        $('.rt-video-popup').magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    }
    if (typeof $.fn.magnificPopup == 'function') {
        if ($('.zoom-gallery').length) {
            $('.zoom-gallery').each(function () { // the containers for all your galleries
                $(this).magnificPopup({
                    delegate: 'a.panpie-popup-zoom', // the selector for gallery item
                    type: 'image',
                    gallery: {
                        enabled: true
                    }
                });
            });
        }
    }


    /* when product quantity changes, update quantity attribute on add-to-cart button */
    $("form.cart").on("change", "input.qty", function () {
        if (this.value === "0")
            this.value = "1";

        $(this.form).find("button[data-quantity]").data("quantity", this.value);
    });

    /* remove old "view cart" text, only need latest one thanks! */
    $(document.body).on("adding_to_cart", function () {
        $("a.added_to_cart").remove();
    });

    /*variable ajax cart end*/
    $('.quantity').on('click', '.plus', function (e) {
        var self = $(this),
            $input = self.prev('input.qty'),
            target = self.parents('form').find('.product_type_simple'),
            val = parseInt($input.val(), 10) + 1;
        target.attr("data-quantity", val);
        $input.val(val);

        return false;
    });

    $('.quantity').on('click', '.minus', function (e) {
        var self = $(this),
            $input = self.next('input.qty'),
            target = self.parents('form').find('.product_type_simple'),
            val = parseInt($input.val(), 10);
        val = (val > 1) ? val - 1 : val;
        target.attr("data-quantity", val);
        $input.val(val);
        return false;
    });

    //variable product select - Food box
    $('.variable-prod-select').select2({
        width: '100%',
        minimumResultsForSearch: -1,
    });
    $('.orderby').select2({minimumResultsForSearch: -1});
		
	// CTO - URL change	
    $('.food-box').on('change', '.variable-prod-select', function (e) {

        var self = $(this),
            slt_value = self.val(),
            slt_attribute = self.data('attribute'),
            wrap = self.closest('.food-box'),
            price_wrap = wrap.find('.item-price'),
            variations = wrap.data('product_variations');
            console.log(variations);
        if (slt_value) {
            var found_variation = variations.find(function (item) {
                return item.attributes["attribute_pa_" + slt_attribute] && item.attributes["attribute_pa_" + slt_attribute] === slt_value
            });
            if (found_variation) {
                price_wrap.html(found_variation.price_html);
                wrap.find(".btn-wrap a.cart-btn, .item-title a").each(function () {
                    var _self = $(this),
                        _url = _self.attr('href'),
                        url = new URL(_url);
                    Object.keys(found_variation.attributes).map(function (item) {
                        url.searchParams.set(item, found_variation.attributes[item])
                    });
                    _self.attr('href', url.toString());
                });
            }
        }
    });

});

function panpie_load_content_area_scripts($) {

    /* progress circle */
    $('.rt-progress-circle').each(function () {
        var startcolor = $(this).data('rtstartcolor'),
            endcolor = $(this).data('rtendcolor'),
            num = $(this).data('rtnum'),
            speed = $(this).data('rtspeed'),
            suffix = $(this).data('rtsuffix');
        $(this).circleProgress({
            value: 1,
            fill: endcolor,
            emptyFill: startcolor,
            thickness: 5,
            size: 140,
            animation: {duration: speed, easing: "circleProgressEasing"},
        }).on('circle-animation-progress', function (event, progress) {
            $(this).find('.rtin-num').html(Math.round(num * progress) + suffix);
        });
    });

}

//function Load
function panpie_content_load_scripts() {
    var $ = jQuery;
    // Preloader
    $('#preloader').fadeOut('slow', function () {
        $(this).remove();
    });

    var windowWidth = $(window).width();

    /* Owl Custom Nav */
    if (typeof $.fn.owlCarousel == 'function') {
        $(".owl-custom-nav .owl-next").on('click', function () {
            $(this).closest('.owl-wrap').find('.owl-carousel').trigger('next.owl.carousel');
        });
        $(".owl-custom-nav .owl-prev").on('click', function () {
            $(this).closest('.owl-wrap').find('.owl-carousel').trigger('prev.owl.carousel');
        });

        $(".rt-owl-carousel").each(function () {
            var options = $(this).data('carousel-options');
            if (panpieObj.rtl == 'yes') {
                options['rtl'] = true; //@rtl
            }
            $(this).owlCarousel(options);
        });
    }

    /* Slick Tab Slider */
    var slickOptions1 = {
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        autoplay: false,
        asNavFor: '.carousel-nav',
        prevArrow: '<span class="slick-prev slick-navigation"><i class="fa fa-angle-left" aria-hidden="true"></i></span>',
        nextArrow: '<span class="slick-next slick-navigation"><i class="fa fa-angle-right" aria-hidden="true"></i></span>'
    }
    var slickOptions2 = {
        slidesToScroll: 1,
        asNavFor: '.carousel-content',
        dots: false,
        arrows: true,
        prevArrow: true,
        nextArrow: true,
        centerMode: true,
        centerPadding: '0px',
        focusOnSelect: true,
        responsive: [{
            breakpoint: 991,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 1
            }
        }, {
            breakpoint: 767,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 1
            }
        }, {
            breakpoint: 479,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }]
    }

    if (panpieObj.rtl == 'yes') {
        // options 1
        slickOptions1.rtl = true;
        slickOptions1.prevArrow = '<span class="slick-prev slick-navigation"><i class="fa fa-angle-right" aria-hidden="true"></i></span>';
        slickOptions1.nextArrow = '<span class="slick-next slick-navigation"><i class="fa fa-angle-left" aria-hidden="true"></i></span>';

        // options 2
        slickOptions2.rtl = true;

    }
    var SlickCarousel = $('.slick-carousel-wrap');
    if (SlickCarousel.length) {
        slickOptions2.slidesToShow = SlickCarousel.data('slide-count') || 5;
        SlickCarousel.find('.carousel-content').slick(slickOptions1);
        SlickCarousel.find('.carousel-nav').slick(slickOptions2);
    }

    imageFunction();

    function imageFunction() {
        $("[data-bg-image]").each(function () {
        let img = $(this).data("bg-image");
            $(this).css({
                backgroundImage: "url(" + img + ")",
            });
        });
    }

    /* Slick Slider */
    if ($.fn.slick) {
        $('.slick-carousel').each(function () {
            let $carousel = $(this);
            $carousel.imagesLoaded(function () {
                var data = $carousel.data('slick'),
                    slidesToShowTab = data.slidesToShowTab,
                    slidesToShowMobile = data.slidesToShowMobile;
                $carousel.slick({
                    centerPadding: '0px',
                    responsive: [{
                        breakpoint: 992,
                        settings: {
                            slidesToShow: slidesToShowTab,
                            slidesToScroll: slidesToShowTab
                        }
                    },
                        {
                            breakpoint: 767,
                            settings: {
                                slidesToShow: slidesToShowMobile,
                                slidesToScroll: slidesToShowMobile
                            }
                        }
                    ]
                });
            });
        });
    }

    /* Counter */
    var counterContainer = $('.counter');
    if (counterContainer.length) {
        console.log(counterContainer);
        counterContainer.counterUp({
            delay: counterContainer.data('rtsteps'),
            time: counterContainer.data('rtspeed')
        });
    }
    var counterContainer = $('.counter2');
    if (counterContainer.length) {
        counterContainer.counterUp({
            delay: 50,
            time: 2000
        });
    }

    /* Circle Bars - Knob */
    if (typeof ($.fn.knob) !== undefined) {
        $('.knob.knob-percent.dial').each(function () {
            var $this = $(this),
                knobVal = $this.attr('data-rel');
            $this.knob({
                'draw': function () {
                },
                'format': function (value) {
                    return value + '%';
                }
            });
            $this.appear(function () {
                $({
                    value: 0
                }).animate({
                    value: knobVal
                }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function () {
                        $this.val(Math.ceil(this.value)).trigger('change');
                    }
                });
            }, {
                accX: 0,
                accY: -150
            });
        });
    }
	
	/* Multiscroll activation code */
    if ($.fn.multiscroll !== undefined) {
        $('#multiscroll').multiscroll({
            verticalCentered: true,
            anchors: ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15'],
            menu: '#msmenu',
            navigation: true,
			navigationPosition: 'right',
            css3: true,
            navigationTooltips: ['First', 'Second', 'Third', '4th', '5th'],
            responsiveWidth: 992, // made responsive
            responsiveExpand: true, // made responsive
            loopBottom: false,
            loopTop: false,
            onLeave: function (index, nextIndex, direction) {
            },
            afterLoad: function (anchorLink, index) {
            },
            afterRender: function () {
            }
        });
    }

    /* Wow Js Init */
    var wow = new WOW({
        boxClass: 'wow',
        animateClass: 'animated',
        offset: 0,
        mobile: false,
        live: true,
        scrollContainer: null,
    });

    new WOW().init();

}

(function ($) {
    "use strict";

    // Window Load+Resize
    $(window).on('load resize', function () {

        // Define the maximum height for mobile menu
        var wHeight = $(window).height();
        wHeight = wHeight - 50;
        $('.mean-nav > ul').css('max-height', wHeight + 'px');

        //initialize swiper when document ready
        $('.rt-swiper-container').each(function () {
            var swiper = $(this),
                autoplay = swiper.data('autoplay'),
                autoplayTimeout = swiper.data('autoplay-timeout') || '',
                speed = swiper.data('speed') || '',
                loop = swiper.data('loop') || true,
                slidesPerView = swiper.data('slides-per-view') || 3,
                spaceBetween = swiper.data('space-between'),
                centeredSlides = swiper.data('centered-slides'),
                rXsmall = swiper.data("r-x-small"),
                rSmall = swiper.data("r-small"),
                rMedium = swiper.data("r-medium"),
                rLarge = swiper.data("r-large"),
                rXlarge = swiper.data("r-x-large");

            var $swiper = new Swiper(swiper, {
                // Optional parameters
                autoplay: autoplay ? true : false,
                autoplayTimeout: autoplayTimeout ? autoplayTimeout : 10000,
                speed: speed ? speed : 2000,
                loop: loop ? true : false,
                slidesPerView: slidesPerView ? slidesPerView : 2,
                spaceBetween: spaceBetween ? spaceBetween : 10,
                centeredSlides: centeredSlides ? true : false,
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                breakpoints: {
                    0: {
                        slidesPerView: rXsmall ? rXsmall : 1,
                    },
                    576: {
                        slidesPerView: rSmall ? rSmall : 2,
                    },
                    768: {
                        slidesPerView: rMedium ? rMedium : 3,
                    },
                    992: {
                        slidesPerView: rLarge ? rLarge : 4,
                    },
                    1200: {
                        slidesPerView: rXlarge ? rXlarge : 5,
                    }
                }
            });
        });


    });

    // Elementor Frontend Load
    $(window).on('elementor/frontend/init', function () {
        if (elementorFrontend.isEditMode()) {
            elementorFrontend.hooks.addAction('frontend/element_ready/widget', function () {
                panpie_content_load_scripts();
            });
        }
    });

    // Window Load
    $(window).on('load', function () {
        panpie_content_load_scripts();
    });

})(jQuery);
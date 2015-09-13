// global disqus variables.
var disqus_shortname = '',
    disqus_identifier = '',
    disqus_title = '',
    disqus_url = '',
    disqus_category_id = '',
    disqus_container_id = '',
    disqus_config = '';

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this,
            args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait || 100);
        if (callNow) func.apply(context, args);
    };
};

;(function($, window, document, undefined) {
    var defaults = {
        popupWidth: 800,
        popupHeight: 400,
        triggerEvent: 'immediately',
        threshold: 300,
        gaEnabled: true,
        gaEventCategory: 'Disqus',
        gtmDataLayerName: 'dataLayer'

    };

    function DisqusEmbed(element, options) {
        this.element = $(element);
        this.settings = $.extend(true, {}, defaults, options);

        disqus_shortname = this.settings.shortname;
        disqus_identifier = this.settings.identifier;
        disqus_title = this.settings.title;
        disqus_url = this.settings.url;
        disqus_category_id = this.settings.categoryId;
        disqus_container_id = this.settings.containerId;

        var that = this;
        disqus_config = function() {
            if (that.settings.apiKey) {
                this.page.api_key = that.settings.apiKey;
            }
            if (that.settings.enableSSO) {
                this.sso = {
                    name: that.settings.siteName,
                    button: '',
                    url: that.settings.loginUrl,
                    logout: that.settings.logoutUrl,
                    width: that.settings.popupWidth,
                    height: that.settings.popupHeight
                };

                if (that.settings.ssoAuth) {
                    this.page.remote_auth_s3 = that.settings.ssoAuth;
                }
            }
            this.language = ''; //@todo
            this.callbacks.onReady.push(function(e) {
                that.trackEvent('Thread Loaded');
            });
            this.callbacks.onNewComment.push(function() {
                that.trackEvent('New Comment');
            });
            this.callbacks.onIdentify.push(function() {
                that.trackEvent('User Logged In');
            });
        };

        this.init();
    }

    DisqusEmbed.prototype = {
        init: function() {
            this.element.one('appear', function() {
                $.ajax({
                    type: 'GET',
                    url: '//' + this.settings.shortname + '.disqus.com/embed.js',
                    dataType: 'script',
                    cache: false,
                    async: true
                });
            }.bind(this));

            switch (this.settings.triggerEvent) {
                case 'immediately':
                    this.element.trigger('appear');
                    break;

                case 'lazyload':
                    this.isInViewport();
                    this.onScroll();
                    break;

                case 'click':
                    this.onClick();
                    break;
            }
        },
        onScroll: function() {
            $(window).scroll(function() {
                this.isInViewport();
            }.bind(this));
        },
        isInViewport: function() {
            if ($.inviewport(this.element, { threshold: this.settings.threshold })) {
                this.element.trigger('appear');
            }
        },
        onClick: function() {
            $('.js-show-comments', this.element).on('click', function () {
                this.element.trigger('appear');
            }.bind(this));
        },
        trackEvent: debounce(function(event) {
            if (!this.settings.gaEnabled) {
                return false;
            }
            var trackingData = {
                hitType: 'event',
                eventCategory: this.settings.gaEventCategory,
                eventLabel: window.location.pathname,
                eventAction: event
            };
            if (typeof window[this.settings.gtmDataLayerName] !== 'undefined') {
                window[this.settings.gtmDataLayerName].push({
                    'event': 'gaEvent',
                    'gaEventCategory': trackingData.eventCategory,
                    'gaEventAction': trackingData.eventAction,
                    'gaEventLabel': trackingData.eventLabel
                });
            }
            if (typeof window['GoogleAnalyticsObject'] !== 'undefined') {
                var _ga = window['GoogleAnalyticsObject'];
                window[_ga]('send', trackingData);
            }
        }, 100),
    };

    $.fn.disqusEmbed = function(options) {
        return this.each(function () {
            if (!$.data(this, 'plugin_disqusEmbed')) {
                $.data(this, 'plugin_disqusEmbed', new DisqusEmbed(this, options));
            }
        });
    };
})(jQuery, window, document);

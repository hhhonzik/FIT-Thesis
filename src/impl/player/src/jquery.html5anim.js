/*
 * animPlayer
 * https://github.com/honzicek/player
 *
 * Copyright (c) 2015 stepaj27
 * Licensed under the MIT license.
 */
(function($) {
  var Controller = require('./app/controller.js');
  // Collection method.
  $.fn.html5anim = function(method) {
    var cache = {}, viewKey = "html5animInstance", methods;
    methods = {
        initialize: function(options) {
          return this.each(initialize);
          function initialize() {
              var $el = $(this);
              options.$el = $el;
              $(this).data(viewKey, new Controller(options));
          }
        },
        play: function () {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.play();
          }
          return $(this);
        },
        pause:  function () {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.pause();
          }
          return $(this);
        },
        playTo:  function (n) {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.animateTo(n);
          }
          return $(this);
        },
        rewindTo:  function (n) {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.rewindTo(n);
          }
          return $(this);
        },
        onPlay:  function (func) {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.onEvent('onPlay', func);
          }
          return $(this);
        },
        onStop: function (func) {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.onEvent('onStop', func);
          }
          return $(this);
        },
        onStop: function (func) {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.onEvent('onStop', func);
          }
          return $(this);
        },
        onFrame:  function (func) {
          var instance = $(this).data(viewKey);
          if (instance) {
            instance.onEvent('onFrame', func);
          }
          return $(this);
        }
    };
    if (methods[method]) {
        return methods[method].apply(this, [].slice.call(arguments, 1));
    } else {
        return methods.initialize.apply(this, arguments);
    }
  };
}(window.jQuery));
